import {Navigate, Route, Routes} from "react-router-dom";
import AppGlobalComponents from "./AppGlobalComponents";

import '../styles/Body.css'
import Button from "../../common/components/Button";


const Body = () => {

    return (
        <div className={`body-container`}>
            <div className={`body-content`}>

                <AppGlobalComponents/>
                <Routes>

                    <Route path="/*" element={
                        <div className="pruebas">

                        </div>
                    }/>

                </Routes>
            </div>
        </div>
    );

};

export default Body;