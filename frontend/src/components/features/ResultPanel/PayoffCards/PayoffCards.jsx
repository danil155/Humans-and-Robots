import { PLAYER_LABEL, PLAYER_COLOR } from "../../../../constants/gameConfig";
import "./PayoffCards.css";

const fmt = (n) =>
    Number(n).toLocaleString("ru-RU", { maximumFractionDigits: 2 });

export function PayoffCards({ payoffs }) {
    if (!payoffs) return null;

    return (
        <div className="payoff-cards">
            {Object.entries(payoffs).map(([key, val]) => (
                <div key={key} className="payoff-card">
                    <p className="payoff-card__label">
                        {PLAYER_LABEL[key] ?? key}
                    </p>
                    <p
                        className="payoff-card__value"
                        style={{ color: PLAYER_COLOR[key] ?? "var(--color-text-primary)" }}
                    >
                        {fmt(val)}
                    </p>
                </div>
            ))}
        </div>
    );
}
