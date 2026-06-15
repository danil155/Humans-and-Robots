import { useState } from "react";
import "./RawJsonPanel.css";

export function RawJsonPanel({ data }) {
    const [open, setOpen] = useState(false);

    if (!data) return null;

    return (
        <div className="raw-json">
            <button
                className="raw-json__toggle"
                onClick={() => setOpen((s) => !s)}
            >
                <i
                    className={`ti ${open ? "ti-eye-off" : "ti-eye"}`}
                    aria-hidden="true"
                />
                {open ? "Скрыть JSON" : "Показать сырой JSON"}
            </button>

            {open && (
                <pre className="raw-json__pre">
          {JSON.stringify(data, null, 2)}
        </pre>
            )}
        </div>
    );
}
