import { useState } from "react";
import { Badge } from "../../../ui";
import { PayoffCards } from "../PayoffCards/PayoffCards";
import { LPDetail } from "../LPDetail/LPDetail";
import { STRATEGY_ICON, STRATEGY_LABEL } from "../../../../constants/gameConfig";
import "./FirmBranch.css";

export function FirmBranch({ firmKey, branch }) {
    const [open, setOpen] = useState(false);
    const isEq = branch?.is_equilibrium;

    return (
        <div className={`firm-branch${isEq ? " firm-branch--equilibrium" : ""}`}>
            <button
                className="firm-branch__header"
                onClick={() => setOpen((o) => !o)}
                aria-expanded={open}
            >
                <div className="firm-branch__header-left">
                    {isEq && <Badge variant="info">равновесие</Badge>}

                    <i
                        className={`ti ${STRATEGY_ICON[firmKey] ?? "ti-point"} firm-branch__firm-icon`}
                        aria-hidden="true"
                    />
                    <span className="firm-branch__firm-key">{firmKey}</span>

                    <i className="ti ti-arrow-right firm-branch__sep" aria-hidden="true" />
                    <span className="firm-branch__response">
                        {STRATEGY_LABEL[branch?.people_response] ?? branch?.people_response}
                    </span>

                    <i className="ti ti-arrow-right firm-branch__sep" aria-hidden="true" />
                    <span className="firm-branch__response">
                        {STRATEGY_LABEL[branch?.regulator_response] ?? branch?.regulator_response}
                    </span>
                </div>

                <i
                    className={`ti ${open ? "ti-chevron-up" : "ti-chevron-down"} firm-branch__chevron`}
                    aria-hidden="true"
                />
            </button>

            {open && (
                <div className="firm-branch__body">
                    <p className="firm-branch__section-label">Выигрыши</p>
                    <PayoffCards payoffs={branch?.expected_payoffs} />

                    {branch?.lp_result && (
                        <>
                            <p className="firm-branch__section-label firm-branch__section-label--mt">
                                LP-оптимум
                            </p>
                            <LPDetail lp={branch.lp_result} />
                        </>
                    )}
                </div>
            )}
        </div>
    );
}
