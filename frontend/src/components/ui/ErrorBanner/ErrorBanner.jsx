import "./ErrorBanner.css";

export function ErrorBanner({ message }) {
    return (
        <div className="error-banner" role="alert">
            <p className="error-banner__heading">
                <i className="ti ti-alert-circle" aria-hidden="true" />
                Ошибка запроса
            </p>
            <p className="error-banner__body">{message}</p>
        </div>
    );
}
