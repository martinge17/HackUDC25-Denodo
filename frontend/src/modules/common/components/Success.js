import PropTypes from 'prop-types';
import '../styles/Success.css'

const Success = ({message, onClose}) => message && (
    <div className="success-container" role="alert">
        {message}
        <button type="button" className="close" data-dismiss="alert" aria-label="Close"
                onClick={() => onClose()}>
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
);

Success.propTypes = {
    message: PropTypes.string,
    onClose: PropTypes.func.isRequired
};

export default Success;
