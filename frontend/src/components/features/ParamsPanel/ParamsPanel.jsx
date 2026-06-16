import { useState } from "react";
import { ParamInput } from "../../ui";
import { PRODUCTION_PARAMS_META, GAME_PARAMS_META } from "../../../constants/gameConfig";
import "./ParamsPanel.css";

const TABS = [
    { id: "prod", label: "ProductionParams", meta: PRODUCTION_PARAMS_META },
    { id: "game", label: "GameParams", meta: GAME_PARAMS_META },
];

export function ParamsPanel({
                                prodParams,
                                gameParams,
                                onProdChange,
                                onGameChange,
                                onSolve,
                                loading,
                            }) {
    const [activeTab, setActiveTab] = useState("prod");

    const activeParams = activeTab === "prod" ? prodParams  : gameParams;
    const activeOnChange = activeTab === "prod" ? onProdChange : onGameChange;
    const activeMeta = TABS.find((t) => t.id === activeTab).meta;

    return (
        <aside className="params-panel">
            <header className="params-panel__header">
                <p className="params-panel__title">Параметры модели</p>
                <p className="params-panel__subtitle">Введите параметры и постройте равновесие</p>
            </header>

            <nav className="params-panel__tabs" role="tablist">
                {TABS.map(({ id, label }) => (
                    <button
                        key={id}
                        role="tab"
                        aria-selected={activeTab === id}
                        className={`params-panel__tab${activeTab === id ? " params-panel__tab--active" : ""}`}
                        onClick={() => setActiveTab(id)}
                    >
                        {label}
                    </button>
                ))}
            </nav>

            <div className="params-panel__fields" role="tabpanel">
                {activeMeta.map(({ key, label }) => (
                    <ParamInput
                        key={key}
                        name={key}
                        label={label}
                        value={activeParams[key]}
                        onChange={activeOnChange}
                    />
                ))}
            </div>

            <button
                className={`params-panel__solve-btn${loading ? " params-panel__solve-btn--loading" : ""}`}
                onClick={onSolve}
                disabled={loading}
            >
                <i
                    className={`ti ${loading ? "ti-loader-2 spin" : "ti-player-play"}`}
                    aria-hidden="true"
                />
                {loading ? "Вычисляем..." : "Построить равновесие"}
            </button>
        </aside>
    );
}
