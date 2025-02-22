import '../styles/Menu.css';
import Button from "./Button";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import * as actions from "../../app/actions";
import { getChatIds } from "../../../backend/denodoService";
import * as selectors from "../../app/selectors";

const Menu = ({ onClick }) => {
    const dispatch = useDispatch();
    const [chats, setChats] = useState([]);
    const id = useSelector(selectors.getChat);

    const handleClick = (chatId) => {
        dispatch(actions.changeChat(chatId));
    };

    const fetchChatIds = async () => {
        try {
            const chatIds = await getChatIds();
            console.log("Chats obtenidos:", chatIds);

            if (Array.isArray(chatIds)) {
                setChats(chatIds);
            } else if (chatIds && chatIds.chats) {
                setChats(chatIds.chats);
            }
        } catch (error) {
            console.error("Error al obtener los chats:", error);
        }
    };

    useEffect(() => {
        fetchChatIds();
    }, []);

    return (
        <div className="menu-container">
            <div className="menu-cabecera">
                <Button id="back" textId={' '} onClick={onClick} />
            </div>

            <div className="menu-options">
                {chats.length > 0 ? (
                    chats.map((chatId) => (
                        <Button
                            key={chatId}
                            id={chatId}
                            textId={chatId}
                            onClick={() => handleClick(chatId)}
                            isSelected={chatId === id }
                        />
                    ))
                ) : (
                    <p>Cargando chats...</p>
                )}
            </div>

            <div className="menu-profile">
                <Button id="d" textId={'d'} onClick={handleClick} />
                <Button id="e" textId={'e'} onClick={handleClick} />
            </div>
        </div>
    );
};

export default Menu;