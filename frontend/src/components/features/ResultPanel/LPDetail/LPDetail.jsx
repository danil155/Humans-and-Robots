import { LP_FIELDS } from "../../../../constants/gameConfig";
import "./LPDetail.css";

const fmt = (n) =>
    Number(n).toLocaleString("ru-RU", { maximumFractionDigits: 2 });

export function LPDetail({ lp }) {
    if (!lp) return null;

    const visible = LP_FIELDS.filter(({ k }) => lp[k] !== undefined);

    return (
        <div className="lp-detail">
            {visible.map(({ k, label }) => (
                <div key={k} className="lp-tile">
                    <p className="lp-tile__label">{label}</p>
                    <p className="lp-tile__value">{fmt(lp[k])}</p>
                </div>
            ))}
        </div>
    );
}
