import '../styles/TextInput.css'

const TextInput = ({id, value, onChange, placeholder = "", rows = 3, required = false, color = false}) => (
    <div className="card">
        <div className={color ? "bg" : ""}></div>
        <div className="content">
            <textarea
                id={id}
                value={value}
                onChange={e => onChange(e.target.value)}
                required={required}
                placeholder={placeholder}
                rows={rows}
            />
        </div>
    </div>
);

export default TextInput;
