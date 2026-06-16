export const DEFAULT_PRODUCTION_PARAMS = {
    p: 220.0,
    L: 2000.0,
    L_soc: 250.0,
    K0: 1500.0,
    D: 5000.0,
    a_m: 1.5,
    a_h: 0.5,
    b_r: 0.8,
    b_h: 0.3,
    gamma: 0.3,
    raw_material_cost: 55.0,
    w_m: 65.0,
    w_h: 100.0,
    insurance_rate: 0.3,
    robot_amortization: 20.0,
    hours_per_person: 40.0,
};

export const DEFAULT_GAME_PARAMS = {
    w_m: 65.0,
    w_h: 100.0,
    effort_cost: 10.0,
    severance: 150.0,
    moral_sat: 5.0,
    stress: 120.0,
    fine: 25000.0,
    subsidy: 20000.0,
    taxes_base: 6000.0,
    gdp_multiplier: 6000.0,
    social_tension_cost: 6000.0,
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
