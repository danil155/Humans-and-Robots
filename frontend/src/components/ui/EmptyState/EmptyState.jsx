import "./EmptyState.css";

export function EmptyState({ icon = "ti-topology-star-3", message }) {
    return (
        <div className="empty-state" role="status">
            <i className={`ti ${icon} empty-state__icon`} aria-hidden="true" />
            <p className="empty-state__message">{message}</p>
        </div>
    );
}
