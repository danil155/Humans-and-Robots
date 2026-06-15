from dataclasses import dataclass
from abc import ABC, abstractmethod

FIRM_STRATEGIES = ['x_low', 'x_high']
PEOPLE_STRATEGIES = ['sabotage', 'adapt']
REG_STRATEGIES = ['audit', 'subsidy']


@dataclass
class ProductionParams:
    """ Параметры для задачи ЛП """

    p: float    # рыночная цена продукции
    L: float
    L_soc: float
    K0: float
    D: float
    a_m: float
    a_h: float
    b_r: float
    b_h: float
    gamma: float

    raw_material_cost: float = 20.0
    w_m: float = 30.0  # ставка ручного труда
    w_h: float = 80.0  # ставка гибрида
    insurance_rate: float = 0.3  # страховые взносы
    robot_amortization: float = 15.0
    hours_per_person: float = 40.0

    @property
    def c_m(self) -> float:
        return self.raw_material_cost + self.w_m * (1 + self.insurance_rate)

    @property
    def c_r(self) -> float:
        return self.raw_material_cost + self.robot_amortization

    @property
    def c_h(self) -> float:
        return self.raw_material_cost + self.w_h * (1 + self.insurance_rate) + self.robot_amortization

    def compute_fire_cost(self, x: float) -> float:
        avg_salary = (self.w_m + self.w_h) / 2
        fired_soc_hours = self.L_soc * (1 - x) * self.gamma
        fired_people = fired_soc_hours / self.hours_per_person

        return fired_people * 4 * avg_salary


@dataclass
class GameParams:
    """ Параметры для расчета выигрышей (payoffs) """

    w_m: float
    w_h: float
    effort_cost: float  # усилия на переобучение
    severance: float    # выходное пособие
    moral_sat: float    # моральное удовлетворение
    stress: float
    fine: float         # штраф Роструда
    subsidy: float
    taxes_base: float   # база налогов
    gdp_multiplier: float   # мултипликатор ВВП
    social_tension_cost: float  # социальная напряженность


@dataclass
class LPOptimum:
    """ Результат решения задачи ЛП """

    y_m: float
    y_r: float
    y_h: float
    z_max: float
    fire_cost: float = 0.0


@dataclass
class Payoffs:
    """ Выигрыши игроков """

    u_firm: float
    u_people: float
    u_regulator: float

    def as_dict(self) -> dict:
        return {'u_firm': self.u_firm, 'u_people': self.u_people, 'u_regulator': self.u_regulator}


class ILPSolver(ABC):
    """ Интерфейс решателя """

    @abstractmethod
    def solve(self, x: float, params: ProductionParams) -> LPOptimum:
        pass
