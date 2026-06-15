import "./Badge.css";

export function Badge({ children, variant = "info" }) {
    return (
        <span className={`badge badge--${variant}`}>
      {children}
    </span>
    );
}
