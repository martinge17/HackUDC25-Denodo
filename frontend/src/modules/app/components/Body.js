import {Route, Routes} from "react-router-dom";
import AppGlobalComponents from "./AppGlobalComponents";

import '../styles/Body.css'
import Menu from "../../common/components/Menu";
import {useEffect, useState} from "react";
import Button from "../../common/components/Button";
import Chat from "./Chat";
import {useDispatch, useSelector} from "react-redux";
import * as selectors from "../selectors";
import * as actions from "../actions";

const Body = () => {

    const menu = useSelector(selectors.menu);
    const dispatch = useDispatch();

    return (
        <div className={`body-container${menu ? "-menu" : ""}`}>
            <div className='menu'>
                {menu ? <Menu onClick={() => dispatch(actions.menu(!menu))}></Menu> :
                    <Button
                        id="back"
                        textId={' '}
                        onClick={() => dispatch(actions.menu(!menu))}
                    />
                }
            </div>
            <div className={`body-content`}>

                <AppGlobalComponents/>
                <Routes>

                    <Route path="/*" element={<Chat/>}/>

                </Routes>
            </div>
        </div>
    );

};

export default Body;