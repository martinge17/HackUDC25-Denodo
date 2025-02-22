import '../styles/Menu.css'
import {useNavigate} from "react-router-dom";
import Button from "./Button";

const Menu = ({onClick}) => {

    const navigate = useNavigate();

    const handleAlgo = () => {
        navigate('/');
    };

    return (
        <div className="menu-container">

            <div className="menu-cabecera">
                <Button
                    id="back"
                    textId={' '}
                    onClick={onClick}
                />
            </div>

            <div className="menu-options">
                <Button
                    id="a"
                    textId={'a'}
                    onClick={handleAlgo}
                />
                <Button
                    id="b"
                    textId={'b'}
                    onClick={handleAlgo}
                />
                <Button
                    id="c"
                    textId={'c'}
                    onClick={handleAlgo}
                />
            </div>

            <div className="menu-profile">
                <Button
                    id="d"
                    textId={'d'}
                    onClick={handleAlgo}
                />
                <Button
                    id="e"
                    textId={'e'}
                    onClick={handleAlgo}
                />
            </div>
        </div>
    );
}

export default Menu;