import { Section } from "../../../ui";
import "./SensitivitySection.css";

export function SensitivitySection({ data }) {
    if (!data)
        return null;

    const entries = Object.entries(data);
    if (!entries.length)
        return null;

    return (
        <Section title="Анализ чувствительности">
            <div className="sensitivity">
                {entries.map(([key, val]) => (
                    <div key={key} className="sensitivity__row">
                        <span className="sensitivity__key">{key}</span>
                        <span className="sensitivity__val">
                            {typeof val === "string" ? val : JSON.stringify(val)}
                        </span>
                    </div>
                ))}
            </div>
        </Section>
    );
}
