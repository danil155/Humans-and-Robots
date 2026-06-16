import numpy as np

from domain.models import ProductionParams, GameParams
from use_cases.game_solver import GameSolver
from infrastructure.lp_solver import ScipyLPSolver
from clusters import COMPANY_CLUSTERS


class ThresholdAnalyzer:
    def __init__(self, base_prod: ProductionParams, base_game: GameParams):
        self.base_prod = base_prod
        self.base_game = base_game
        self.solver = ScipyLPSolver()

    def analyze_w_h_threshold(self, w_m: float, w_h_range: list[float]) -> dict:
        """ При какой зарплате гибридов меняется равновесие """
        results = []

        for w_h in w_h_range:
            game = GameParams(**self.base_game.__dict__)
            game.w_h = w_h

            prod = ProductionParams(**self.base_prod.__dict__)
            prod.w_h = w_h

            solver = GameSolver(self.solver, prod, game)
            result = solver.solve_backward_induction()

            results.append({
                'w_h': w_h,
                'equilibrium': result['equilibrium_path'],
                'firm_payoff': result['equilibrium_payoffs']['Firm'],
                'people_payoff': result['equilibrium_payoffs']['People'],
                'regulator_payoff': result['equilibrium_payoffs']['Regulator']
            })

        return {
            'parameter': 'w_h',
            'values': w_h_range,
            'results': results,
            'threshold': self._find_threshold(results, 'w_h')
        }

    def analyze_fine_threshold(self, fine_range: list[float]) -> dict:
        """ При каком штрафе фирма выбирает x_low вместо x_high """

        results = []

        for fine in fine_range:
            game = GameParams(**self.base_game.__dict__)
            game.fine = fine

            solver = GameSolver(self.solver, self.base_prod, game)
            result = solver.solve_backward_induction()

            results.append({
                'fine': fine,
                'equilibrium': result['equilibrium_path'],
                'firm_payoff': result['equilibrium_payoffs']['Firm']
            })

        return {
            'parameter': 'fine',
            'values': fine_range,
            'results': results,
            'threshold': self._find_threshold(results, 'fine')
        }

    def analyze_robot_cost_threshold(self, robot_cost_range: list[float]) -> dict:
        """ При какой стоимости роботов меняется стратегия """

        results = []

        for robot_cost in robot_cost_range:
            prod = ProductionParams(**self.base_prod.__dict__)
            prod.robot_amortization = robot_cost

            solver = GameSolver(self.solver, prod, self.base_game)
            result = solver.solve_backward_induction()

            results.append({
                'robot_cost': robot_cost,
                'equilibrium': result['equilibrium_path'],
                'firm_payoff': result['equilibrium_payoffs']['Firm']
            })

        return {
            'parameter': 'robot_amortization',
            'values': robot_cost_range,
            'results': results,
            'threshold': self._find_threshold(results, 'robot_cost')
        }

    @staticmethod
    def _find_threshold(results: list[dict], param: str) -> dict:
        thresholds = []

        for i in range(1, len(results)):
            prev_strat = results[i - 1]['equilibrium'][0]
            curr_strat = results[i]['equilibrium'][0]

            if prev_strat != curr_strat:
                thresholds.append({
                    'param_value': results[i][param],
                    'from_strategy': prev_strat,
                    'to_strategy': curr_strat,
                    'interval': (results[i - 1][param], results[i][param])
                })

        return {
            'thresholds': thresholds,
            'total_changes': len(thresholds)
        }

    def generate_heatmap_data(self) -> dict:
        w_h_values = np.linspace(30, 150, 10)
        fine_values = np.linspace(1000, 50000, 10)

        heatmap = []

        for w_h in w_h_values:
            row = []
            for fine in fine_values:
                game = GameParams(**self.base_game.__dict__)
                game.w_h = w_h
                game.fine = fine

                prod = ProductionParams(**self.base_prod.__dict__)
                prod.w_h = w_h

                solver = GameSolver(self.solver, prod, game)
                result = solver.solve_backward_induction()

                row.append({
                    'firm_strategy': result['equilibrium_path'][0],
                    'firm_payoff': result['equilibrium_payoffs']['Firm']
                })
            heatmap.append(row)

        return {
            'w_h_values': w_h_values.tolist(),
            'fine_values': fine_values.tolist(),
            'heatmap': heatmap
        }


def analyze_all_clusters():
    results = {}

    for cluster_name, cluster_data in COMPANY_CLUSTERS.items():
        print(f'\n{"=" * 60}')
        print(f'Анализ: {cluster_data["name"]}')
        print(f'{"=" * 60}')

        prod = ProductionParams(**cluster_data['production_params'])
        game = GameParams(**cluster_data['game_params'])

        solver = GameSolver(ScipyLPSolver(), prod, game)
        result = solver.solve_backward_induction()

        print(f'Равновесие: {"  ".join(result["equilibrium_path"])}')
        print(f'Выигрыш фирмы: {result["equilibrium_payoffs"]["Firm"]:.2f}')

        analyzer = ThresholdAnalyzer(prod, game)

        fine_results = analyzer.analyze_fine_threshold(
            list(np.linspace(1000, 50000, 20))
        )

        if fine_results['threshold']['total_changes'] > 0:
            print(f'Критический штраф: {fine_results["threshold"]["thresholds"][0]["param_value"]:.0f}')

        results[cluster_name] = {
            'equilibrium': result['equilibrium_path'],
            'payoffs': result['equilibrium_payoffs'],
            'thresholds': fine_results['threshold']
        }

    return results
