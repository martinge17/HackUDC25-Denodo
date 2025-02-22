import {Route, Routes} from "react-router-dom";
import AppGlobalComponents from "./AppGlobalComponents";

import '../styles/Body.css'
import TextInput from "../../common/components/TextInput";
import SendButton from "../../common/components/SendButton";
import Menu from "../../common/components/Menu";
import {useState} from "react";
import Button from "../../common/components/Button";

const Body = () => {

    const[menu, setMenu] = useState(true)
    const [prueba, setPrueba] = useState('');

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

                    <Route path="/*" element={
                        <div className="pruebas">
                            <TextInput
                                color={true}
                                onChange={setPrueba}
                                placeholder="Type your question here."
                                value={prueba}
                            >
                            </TextInput>
                            <SendButton onClick={() => setPrueba("")}></SendButton>
                        </div>
                    }/>

                </Routes>
            </div>
        </div>
    );

};

export default Body;