import React from 'react';
import '../styles/Button.css';
import {FormattedMessage} from 'react-intl';

const Button = ({id, textId = "prueba", type = "button", onClick, isSelected = false}) => {
    return (
        <button
            id={id}
            className={`${isSelected ? "button-selected" : "button"}`}
            type={type}
            onClick={onClick}
        >
            <FormattedMessage id={textId}/>
        </button>
    );
};

export default Button;