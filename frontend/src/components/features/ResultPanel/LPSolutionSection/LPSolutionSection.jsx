import { Section } from "../../../ui";
import "./LPSolutionSection.css";

const fmt = (n) => {
    if (n === undefined || n === null) return "—";
    return Number(n).toLocaleString("ru-RU", {
        minimumFractionDigits: 4,
        maximumFractionDigits: 4
    });
};

const PI_LABELS = {
    pi_1: "Трудовое ограничение",
    pi_2: "Роботизированное ограничение",
    pi_3: "Рыночный спрос",
    pi_4: "Социальное ограничение",
};

const PI_HINTS = {
    pi_1: "Ценность 1 человеко-часа",
    pi_2: "Ценность 1 машино-часа",
    pi_3: "Ценность 1 единицы спроса",
    pi_4: "Цена социальной защиты",
};

const PI_COLORS = {
    pi_1: "#2196F3",
    pi_2: "#4CAF50",
    pi_3: "#FF9800",
    pi_4: "#DC3545",
};

export function LPSolutionSection({ lpSolution }) {
    if (!lpSolution) return null;

    const piEntries = Object.entries(PI_LABELS)
        .filter(([key]) => key in lpSolution)
        .map(([key, label]) => ({
            key,
            label,
            value: lpSolution[key],
            hint: PI_HINTS[key],
            color: PI_COLORS[key],
        }));

    if (piEntries.length === 0) return null;

    return (
        <Section title="Двойственные оценки">
            <div className="pi-cards">
                {piEntries.map(({ key, label, value, hint, color }) => (
                    <div key={key} className="pi-card">
                        <p className="pi-card__label">
                            {label}
                        </p>
                        <p className="pi-card__value" style={{ color }}>
                            {fmt(value)}
                        </p>
                        <p className="pi-card__hint">{hint}</p>
                    </div>
                ))}
            </div>
        </Section>
    );
}
