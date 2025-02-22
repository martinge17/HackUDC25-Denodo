import {Route, Routes} from "react-router-dom";
import AppGlobalComponents from "./AppGlobalComponents";

import '../styles/Body.css'
import Menu from "../../common/components/Menu";
import {useEffect, useState} from "react";
import Button from "../../common/components/Button";
import Chat from "./Chat";

const Body = () => {

    const[menu, setMenu] = useState(true)

    return (
        <div className={`body-container${menu ? "-menu" : ""}`}>
            <div className='menu'>
                {menu ? <Menu onClick={() => setMenu(!menu)}></Menu> :
                    <Button
                        id="back"
                        textId={' '}
                        onClick={() => setMenu(!menu)}
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