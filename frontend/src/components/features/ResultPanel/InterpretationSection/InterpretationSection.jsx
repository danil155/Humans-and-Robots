import { Section } from "../../../ui";
import "./InterpretationSection.css";

export function InterpretationSection({ text }) {
    if (!text) return null;

    return (
        <Section title="Интерпретация">
            <p className="interpretation__text">{text}</p>
        </Section>
    );
}
