import { STRATEGY_ICON, STRATEGY_LABEL, PATH_PLAYERS } from "../../../../constants/gameConfig";
import "./EquilibriumPath.css";

export function EquilibriumPath({ path }) {
    if (!path?.length) return null;

    return (
        <div className="eq-path" role="list">
            {path.map((strategy, i) => (
                <div key={i} className="eq-path__step" role="listitem">
                    <div className="eq-path__node">
                        <span className="eq-path__player">{PATH_PLAYERS[i]}</span>
                        <div className="eq-path__chip">
                            <i
                                className={`ti ${STRATEGY_ICON[strategy] ?? "ti-point"} eq-path__chip-icon`}
                                aria-hidden="true"
                            />
                            <span className="eq-path__chip-label">
                                {STRATEGY_LABEL[strategy] ?? strategy}
                            </span>
                        </div>
                    </div>
                    {i < path.length - 1 && (
                        <i className="ti ti-arrow-right eq-path__arrow" aria-hidden="true" />
                    )}
                </div>
            ))}
        </div>
    );
}
