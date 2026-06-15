import "./Section.css";

export function Section({ title, children }) {
    return (
        <section className="section">
            <p className="section__title">{title}</p>
            {children}
        </section>
    );
}
