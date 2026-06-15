import "./ParamInput.css";

export function ParamInput({ label, name, value, onChange }) {
    return (
        <div className="param-input">
            <label className="param-input__label" htmlFor={`param-${name}`}>
                {label}
            </label>
            <input
                id={`param-${name}`}
                className="param-input__field"
                type="number"
                step="any"
                value={value}
                onChange={(e) => onChange(name, parseFloat(e.target.value) || 0)}
            />
        </div>
    );
}
