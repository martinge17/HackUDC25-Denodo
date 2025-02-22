import '../styles/Menu.css';
import Button from "./Button";
import { useEffect, useState, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import * as actions from "../../app/actions";
import { getChatIds } from "../../../backend/denodoService";
import * as selectors from "../../app/selectors";

const Menu = ({ onClick }) => {
    const dispatch = useDispatch();
    const [chats, setChats] = useState([]);
    const id = useSelector(selectors.getChat);
    const lastId = useSelector(selectors.getLastChat);

    const handleClick = useCallback((chatId) => {
        dispatch(actions.changeChat(chatId));

        if (chatId === lastId + 1) {
            dispatch(actions.changeLastChat(chatId));
        }
    }, [dispatch, lastId]);

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
    }, [id]);

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
                            isSelected={chatId === id}
                        />
                    ))
                ) : (
                    <Button
                        key={0}
                        id={1}
                        textId={1}
                        onClick={() => handleClick(1)}
                        isSelected={true}
                    />
                )}
            </div>

            <div className="menu-profile">
                <Button id="d" textId={'menu-new-chat'} onClick={() => handleClick(lastId + 1)} />
            </div>
        </div>
    );
};

export default Menu;