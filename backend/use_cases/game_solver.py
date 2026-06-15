from domain.models import (
    ILPSolver,
    ProductionParams,
    GameParams,
    Payoffs,
    FIRM_STRATEGIES,
    PEOPLE_STRATEGIES,
    REG_STRATEGIES
)


class GameSolver:
    def __init__(self, lp_solver: ILPSolver, prod_params: ProductionParams, game_params: GameParams):
        self._lp_solver = lp_solver
        self._prod_params = prod_params
        self._game_params = game_params

        self._x_map = {'x_low': 0.2, 'x_high': 0.8}

    def solve_backward_induction(self) -> dict:
        """ Поиск совершенного в подиграх равновесия Нэша """

        solution_tree = {}

        best_firm_action = None
        max_firm_payoff = float('-inf')

        for s_firm in FIRM_STRATEGIES:
            best_people_action = None
            max_people_payoff = float('-inf')

            people_results = {}

            for s_people in PEOPLE_STRATEGIES:
                best_reg_action = None
                max_reg_payoff = float('-inf')
                best_reg_payoffs = None

                for s_reg in REG_STRATEGIES:
                    payoffs = self._calculate_payoffs(s_firm, s_people, s_reg)

                    if payoffs.u_regulator > max_reg_payoff:
                        max_reg_payoff = payoffs.u_regulator
                        best_reg_action = s_reg
                        best_reg_payoffs = payoffs

                people_results[s_people] = {
                    'regulator_response': best_reg_action,
                    'payoffs': best_reg_payoffs
                }

                if best_reg_payoffs.u_people > max_people_payoff:
                    max_people_payoff = best_reg_payoffs.u_people
                    best_people_action = s_people
                    best_people_payoffs = best_reg_payoffs
                    best_people_reg_response = best_reg_action

            solution_tree[s_firm] = {
                'people_response': best_people_action,
                'regulator_response': best_people_reg_response,
                'expected_payoffs': best_people_payoffs.as_dict(),
                'lp_result': self._get_lp_debug_info(s_firm)
            }

            if best_people_payoffs.u_firm > max_firm_payoff:
                max_firm_payoff = best_people_payoffs.u_firm
                best_firm_action = s_firm
                best_firm_payoffs = best_people_payoffs

        return {
            'equilibrium_path': [
                best_firm_action,
                solution_tree[best_firm_action]['people_response'],
                solution_tree[best_firm_action]['regulator_response']
            ],
            'equilibrium_payoffs': {
                'Firm': best_firm_payoffs.u_firm,
                'People': best_firm_payoffs.u_people,
                'Regulator': best_firm_payoffs.u_regulator
            },
            "full_tree_eval": solution_tree
        }

    def analyze_equilibrium(self, result: dict) -> dict:
        eq_path = result['equilibrium_path']
        eq_payoffs = result['equilibrium_payoffs']
        full_tree = result['full_tree_eval']

        lp_info = full_tree[eq_path[0]]['lp_result']

        analysis = {
            'explanation': {},
            'lp_insights': {},
            'sensitivity': {}
        }

        analysis['explanation']['firm'] = (
            f'Фирма выбрала {eq_path[0]}, получив прибыль {eq_payoffs["Firm"]:.2f}. '
            f'Операционная прибыль (до вычета издержек на сокращение) = {lp_info["operational_profit"]:.2f}, '
            f'издержки на сокращение = {lp_info["fire_cost"]:.2f}.'
        )

        w_h_net = self._game_params.w_h - self._game_params.effort_cost
        sabotage_payoff = self._game_params.severance - self._game_params.stress

        sabotage_with_audit = sabotage_payoff + self._game_params.moral_sat

        analysis['explanation']['people'] = (
            f'Сравнение выигрышей людей:\n'
            f'  - Адаптация: W_h - effort_cost = {self._game_params.w_h:.2f} - '
            f'{self._game_params.effort_cost:.2f} = {w_h_net:.2f}\n'
            f'  - Саботаж без проверки: severance - stress = {self._game_params.severance:.2f} - '
            f'{self._game_params.stress:.2f} = {sabotage_payoff:.2f}\n'
            f'  - Саботаж с проверкой: + moral_sat = {sabotage_with_audit:.2f}\n'
            f'Выбрано: {eq_path[1]}'
        )

        if eq_path[2] == 'subsidy':
            analysis['explanation']['regulator'] = (
                f'Регулятор выбрал субсидию, т.к. люди адаптируются, социальная напряженность = 0, '
                f'выигрыш = {eq_payoffs["Regulator"]:.2f}.'
            )
        else:
            analysis['explanation']['regulator'] = (
                f'Регулятор выбрал проверку, чтобы снизить социальную напряженность ценой штрафа.'
            )

        # Анализ чувствительности
        analysis['sensitivity']['critical_fine'] = (
            f'Штраф ({self._game_params.fine}) достаточно высок, чтобы '
            f'стимулировать Фирму к субсидиям, а не проверкам.'
        )

        base_firm_payoff = eq_payoffs['Firm']

        fine_sensitivity = self._check_fine_sensitivity(base_firm_payoff)
        analysis['sensitivity']['fine'] = fine_sensitivity

        return analysis

    def _check_fine_sensitivity(self, base_firm_payoff: float) -> str:
        """ Проверяет, изменится ли выбор Фирмы при удвоении штрафа """

        current_fine = self._game_params.fine
        self._game_params.fine *= 2
        self._game_params.fine = current_fine

        return f'При удвоении штрафа ({current_fine * 2:.0f}) Фирма может отказаться от стратегии ' \
               f'{base_firm_payoff > 0}'

    def _calculate_payoffs(self, s_firm: str, s_people: str, s_reg: str) -> Payoffs:
        x = self._x_map[s_firm]
        lp_res = self._lp_solver.solve(x, self._prod_params)

        u_firm = lp_res.z_max
        if s_reg == 'audit':
            u_firm -= self._game_params.fine
        elif s_reg == 'subsidy':
            u_firm += self._game_params.subsidy

        if s_people == 'sabotage':
            u_people = self._game_params.severance - self._game_params.stress
            if s_reg == 'audit':
                u_people += self._game_params.moral_sat
        else:
            u_people = self._game_params.w_h - self._game_params.effort_cost

        u_reg = self._game_params.taxes_base + (x * self._game_params.gdp_multiplier)
        if s_people == 'sabotage':
            u_reg -= self._game_params.social_tension_cost
        if s_reg == 'subsidy':
            u_reg -= self._game_params.subsidy

        return Payoffs(
            u_firm=u_firm,
            u_people=u_people,
            u_regulator=u_reg
        )

    def _get_lp_debug_info(self, s_firm: str) -> dict:
        x = self._x_map[s_firm]
        lp_res = self._lp_solver.solve(x, self._prod_params)

        return {
            'x': x,
            'fire_cost': lp_res.fire_cost,
            'operational_profit': lp_res.z_max + lp_res.fire_cost,
            'y_m': lp_res.y_m,
            'y_r': lp_res.y_r,
            'y_h': lp_res.y_h,
            'c_m': self._prod_params.c_m,
            'c_r': self._prod_params.c_r,
            'c_h': self._prod_params.c_h
        }
