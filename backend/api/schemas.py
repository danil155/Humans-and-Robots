from pydantic import BaseModel, Field


class ProductionParamsRequest(BaseModel):
    p: float = Field(100.0, description='Рыночная цена')
    L: float = Field(1000.0, description='Доступный фонд времени')
    L_soc: float = Field(200.0, description='Социально защищенные часы')
    K0: float = Field(500.0, description='Начальная мощность роботов')
    D: float = Field(2000.0, description='Рыночный спрос')
    a_m: float = Field(2.0, description='Трудоемкость ручного труда')
    a_h: float = Field(1.0, description='Трудоемкость гибрида')
    b_r: float = Field(1.0, description='Роботоемкость роботов')
    b_h: float = Field(0.5, description='Роботоемкость гибрида')
    gamma: float = Field(1.0, description='Строгость соц. защиты')
    raw_material_cost: float = Field(20.0, description='Стоимость сырья')
    w_m: float = Field(30.0, description='Ставка ручного труда')
    w_h: float = Field(80.0, description='Ставка гибрида')
    insurance_rate: float = Field(0.3, description='Страховые взносы')
    robot_amortization: float = Field(15.0, description='Амортизация роботов')
    hours_per_person: float = Field(40.0, description='Часов на человека')


class GameParamsRequest(BaseModel):
    w_m: float = Field(30.0, description='ЗП ручного труда')
    w_h: float = Field(80.0, description='ЗП гибрида')
    effort_cost: float = Field(20.0, description='Затраты на переобучение')
    severance: float = Field(150.0, description='Выходное пособие')
    moral_sat: float = Field(50.0, description='Моральное удовлетворение')
    stress: float = Field(100.0, description='Стресс при увольнении')
    fine: float = Field(10000.0, description='Штраф Роструда')
    subsidy: float = Field(5000.0, description='Субсидия')
    taxes_base: float = Field(1000.0, description='База налогов')
    gdp_multiplier: float = Field(2000.0, description='Мультипликатор ВВП')
    social_tension_cost: float = Field(8000.0, description='Социальная напряженность')


class SolveGameRequest(BaseModel):
    production_params: ProductionParamsRequest
    game_params: GameParamsRequest


class StrategyResponse(BaseModel):
    firm: str = Field(..., description='Стратегия Фирмы: x_low или x_high')
    people: str = Field(..., description='Стратегия Людей: sabotage или adapt')
    regulator: str = Field(..., description='Стратегия Регулятора: audit или subsidy')


class PayoffsResponse(BaseModel):
    u_firm: float = Field(..., description='Выигрыш Фирмы')
    u_people: float = Field(..., description='Выигрыш Людей')
    u_regulator: float = Field(..., description='Выигрыш Регулятора')


class LPSolutionResponse(BaseModel):
    y_m: float = Field(..., description='Объем ручного производства')
    y_r: float = Field(..., description='Объем роботизированного производства')
    y_h: float = Field(..., description='Объем гибридного производства')
    z_max: float = Field(..., description='Максимальная прибыль')
    fire_cost: float = Field(0.0, description='Издержки на сокращение')
    operational_profit: float = Field(..., description='Операционная прибыль')
    c_m: float = Field(..., description='Издержки ручного труда')
    c_r: float = Field(..., description='Издержки роботов')
    c_h: float = Field(..., description='Издержки гибрида')
    pi_1: float = Field(..., description='Трудовая двойственная переменная')
    pi_2: float = Field(..., description='Роботизированная двойственная переменная')
    pi_3: float = Field(..., description='Рыночная двойственная переменная')
    pi_4: float = Field(..., description='Социальная двойственная переменная')


class FullTreeEvalItem(BaseModel):
    people_response: str
    regulator_response: str
    expected_payoffs: dict[str, float]
    lp_result: dict[str, object]


class SolveGameResponse(BaseModel):
    equilibrium: StrategyResponse = Field(..., description='Равновесные стратегии')
    payoffs: PayoffsResponse = Field(..., description='Выигрыши в равновесии')
    lp_solution: LPSolutionResponse = Field(..., description='Решение ЛП')
    full_tree_eval: dict[str, FullTreeEvalItem] | None = Field(None, description='Полное дерево игры')
    analysis: dict[str, object] | None = Field(None, description='Анализ и интерпретация')
