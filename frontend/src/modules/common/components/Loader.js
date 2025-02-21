import PropTypes from 'prop-types';

import '../styles/Loader.css';

const Loader = ({loading}) => loading && (
    <div id="floatingCirclesG">
        <div className="f_circleG" id="frotateG_01"></div>
        <div className="f_circleG" id="frotateG_02"></div>
        <div className="f_circleG" id="frotateG_03"></div>
        <div className="f_circleG" id="frotateG_04"></div>
        <div className="f_circleG" id="frotateG_05"></div>
        <div className="f_circleG" id="frotateG_07"></div>
        <div className="f_circleG" id="frotateG_08"></div>
    </div>
);

Loader.propTypes = {
    loading: PropTypes.bool.isRequired
};

export default Loader;
