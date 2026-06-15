export const DEFAULT_PRODUCTION_PARAMS = {
    p: 100.0,
    L: 500.0,
    L_soc: 400.0,
    K0: 1000.0,
    D: 200.0,
    a_m: 1.5,
    a_h: 2.0,
    b_r: 1.2,
    b_h: 0.8,
    gamma: 0.5,
    raw_material_cost: 20.0,
    w_m: 30.0,
    w_h: 80.0,
    insurance_rate: 0.3,
    robot_amortization: 15.0,
    hours_per_person: 40.0,
};

export const DEFAULT_GAME_PARAMS = {
    w_m: 30.0,
    w_h: 80.0,
    effort_cost: 50.0,
    severance: 60.0,
    moral_sat: 20.0,
    stress: 30.0,
    fine: 10000.0,
    subsidy: 5000.0,
    taxes_base: 1000.0,
    gdp_multiplier: 1.5,
    social_tension_cost: 200.0,
};

export const PRODUCTION_PARAMS_META = [
    { key: "p", label: "Рыночная цена (p)" },
    { key: "L", label: "Труд (L)" },
    { key: "L_soc", label: "Соц. труд (L_soc)" },
    { key: "K0", label: "Капитал (K0)" },
    { key: "D", label: "Спрос (D)" },
    { key: "a_m", label: "a_m" },
    { key: "a_h", label: "a_h" },
    { key: "b_r", label: "b_r" },
    { key: "b_h", label: "b_h" },
    { key: "gamma", label: "Gamma (γ)" },
    { key: "raw_material_cost", label: "Сырьё" },
    { key: "w_m", label: "Ставка ручного труда (w_m)" },
    { key: "w_h", label: "Ставка гибрида (w_h)" },
    { key: "insurance_rate", label: "Страховые взносы" },
    { key: "robot_amortization", label: "Амортизация робота" },
    { key: "hours_per_person", label: "Часов на человека" },
];

export const GAME_PARAMS_META = [
    { key: "w_m", label: "Ставка ручного труда (w_m)" },
    { key: "w_h", label: "Ставка гибрида (w_h)" },
    { key: "effort_cost", label: "Усилия переобучения" },
    { key: "severance", label: "Выходное пособие" },
    { key: "moral_sat", label: "Моральное удовлетворение" },
    { key: "stress", label: "Стресс" },
    { key: "fine", label: "Штраф Роструда" },
    { key: "subsidy", label: "Субсидия" },
    { key: "taxes_base", label: "База налогов" },
    { key: "gdp_multiplier", label: "Мультипликатор ВВП" },
    { key: "social_tension_cost", label: "Социальная напряжённость" },
];

export const STRATEGY_LABEL = {
    x_low: "x_low",
    x_high: "x_high",
    sabotage: "Саботаж",
    adapt: "Адаптация",
    audit: "Проверка",
    subsidy: "Субсидия",
};

export const STRATEGY_ICON = {
    x_low: "ti-arrow-down",
    x_high: "ti-arrow-up",
    sabotage: "ti-flame",
    adapt: "ti-refresh",
    audit: "ti-clipboard-check",
    subsidy: "ti-coin",
};

export const PLAYER_LABEL = {
    u_firm: "Фирма",
    u_people: "Люди",
    u_regulator: "Регулятор",
    Firm: "Фирма",
    People: "Люди",
    Regulator: "Регулятор",
};

export const PLAYER_COLOR = {
    u_firm: "var(--color-text-info)",
    u_people: "var(--color-text-success)",
    u_regulator: "var(--color-text-warning)",
    Firm: "var(--color-text-info)",
    People: "var(--color-text-success)",
    Regulator: "var(--color-text-warning)",
};

export const PATH_PLAYERS = ["Фирма", "Люди", "Регулятор"];

export const LP_FIELDS = [
    { k: "x", label: "x (авто.)" },
    { k: "operational_profit", label: "Опер. прибыль" },
    { k: "fire_cost", label: "Издержки сокращения" },
    { k: "y_m", label: "y_m" },
    { k: "y_r", label: "y_r" },
    { k: "y_h", label: "y_h" },
    { k: "c_m", label: "c_m" },
    { k: "c_r", label: "c_r" },
    { k: "c_h", label: "c_h" },
];
