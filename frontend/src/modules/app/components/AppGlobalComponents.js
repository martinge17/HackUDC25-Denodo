import {useSelector, useDispatch} from 'react-redux';

import * as actions from '../actions';
import * as selectors from '../selectors';
import ErrorDialog from "../../common/components/ErrorDialog";
import Loader from "../../common/components/Loader";

const ConnectedErrorDialog = () => {

    const error = useSelector(selectors.getError);
    const dispatch = useDispatch();

    return <ErrorDialog error={error}
                        onClose={() => dispatch(actions.error(null))}/>

};

const ConnectedLoader = () => {

    const loading = useSelector(selectors.isLoading);

    return <Loader loading={loading}/>

};

const AppGlobalComponents = () => (

    <div>
        <ConnectedErrorDialog/>
        <ConnectedLoader/>
    </div>

);

export default AppGlobalComponents;
