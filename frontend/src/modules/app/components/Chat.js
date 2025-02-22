import { FormattedMessage } from 'react-intl';
import '../styles/Chat.css';
import TextInput from "../../common/components/TextInput";
import SendButton from "../../common/components/SendButton";
import { useEffect, useState } from "react";
import Loader from "../../common/components/Loader";
import ChatLine from "../../common/components/ChatLine";
import { getChatHistory, answerQuestion } from "../../../backend/denodoService";
import {useDispatch, useSelector} from "react-redux";
import * as selectors from '../selectors';
import * as actions from "../actions";

const Chat = () => {
    const chatId = useSelector(selectors.getChat);
    const dispatch = useDispatch();
    const menu = useSelector(selectors.menu);

    const [question, setQuestion] = useState("");
    const [isFirst, setIsFirst] = useState(true);


    const [history, setHistory] = useState([]);
    const [response, setResponse] = useState(null);
    const [backendErrors, setBackendErrors] = useState(null);
    const [loading, setLoading] = useState(false);
    const [prueba, setPrueba] = useState("");

    const fetchHistory = async () => {
        try {
            const chatHistory = await getChatHistory(chatId);
            setHistory(chatHistory);
            if (chatHistory && chatHistory.length > 0) {
                setIsFirst(false);
            } else(setIsFirst(true))
        } catch (error) {
            console.error("Error al obtener historial:", error);
        }
    };

    useEffect(() => {
        if (chatId) {
            setHistory([]);
            setResponse(null);
            setPrueba("");
            setBackendErrors(null);
            setLoading(false);
            fetchHistory();
        }
    }, [chatId]);

    const handleQuestion = async (question) => {
        setLoading(true);
        setResponse(null);
        setBackendErrors(null);
        try {
            if (menu && isFirst) {dispatch(actions.menu(!menu))}
            const answer = await answerQuestion(chatId, question);
            setResponse(answer);
            setIsFirst(false);
        } catch (errors) {
            console.error(errors);
            setBackendErrors(errors);
        } finally {
            setLoading(false);
            setPrueba(question);
            setQuestion("");
            fetchHistory();
        }
    };

    return (
        <div className="chat-container">
            <div className={`${isFirst ? "chat-container-textinput-first" : "chat-container-textinput"}`}>
                <div className="chat-container-chats">
                    {
                        // Si no hay mensajes y se está cargando (primer mensaje) se muestra el spinner centrado
                        loading && history.length === 0 ? (
                            <div className="loader-center">
                                <Loader loading />
                            </div>
                        ) : (
                            // Si hay historial, se renderiza cada mensaje
                            history && history.length > 0 ? (
                                history.map((msg) => (
                                    <div key={msg.msg_id} className="request">
                                        <ChatLine texto={msg.pregunta} rigth={true} />
                                        <ChatLine texto={msg.respuesta} rigth={false} />
                                    </div>
                                ))
                            ) : (
                                // Si no hay historial pero ya se obtuvo una respuesta (primer mensaje enviado)
                                response != null && (
                                    <div className="request">
                                        <ChatLine texto={prueba} rigth={true} />
                                        <ChatLine texto={response} rigth={false} />
                                    </div>
                                )
                            )
                        )
                    }
                </div>
                {
                    // El área del input se muestra solo si NO estamos en el primer mensaje y cargando.
                    // Es decir: si es el primer mensaje y se está cargando, se oculta el input.
                    !(loading && history.length === 0) && (
                        <div className={`${isFirst ? "chat-textinput-first" : "chat-textinput"}`}>
                            <TextInput
                                color={true}
                                onChange={setQuestion}
                                placeholder="Type your question here."
                                value={question}
                            />
                            {
                                history && history.length > 0 ? (
                                    loading
                                        ? <Loader loading />
                                        : <SendButton onClick={() => handleQuestion(question)} />
                                ) : (
                                    loading
                                        ? null
                                        : <SendButton onClick={() => handleQuestion(question)} />
                                )
                            }
                        </div>
                    )
                }
            </div>
        </div>
    );
};

export default Chat;