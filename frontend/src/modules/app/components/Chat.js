import {FormattedMessage} from 'react-intl';
import '../styles/Chat.css'
import TextInput from "../../common/components/TextInput";
import SendButton from "../../common/components/SendButton";
import {useEffect, useState} from "react";
import backend from "../../../backend";
import Loader from "../../common/components/Loader";

const Chat = () => {

    const [chatId, setChatId] = useState(0);
    const [question, setQuestion] = useState("");
    const [isFirst, setIsFirst] = useState(true);

    const [response, setResponse] = useState(null);
    const [backendErrors, setBackendErrors] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        //función que mira si el chat tiene contenido, si lo tiene, pone isFirst a false
    }, [chatId]);

    const handleQuestion = async (question) => {
        setLoading(true);
        setResponse(null);
        setBackendErrors(null);

        try {
            const response = await backend.denodoService.answerQuestion(question);
            console.log(response);
            setResponse(response);
            setIsFirst(false);
        } catch (errors) {
            console.log(errors);
            setBackendErrors(errors);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div className="chat-container">

            <div className={`${isFirst ? "chat-container-textinput-first" : "chat-container-textinput"}`}>
                {loading && <Loader loading/>}

                {!loading &&

                    <div className={`${isFirst ? "chat-textinput-first" : "chat-textinput"}`}>
                        <TextInput
                            color={true}
                            onChange={setQuestion}
                            placeholder="Type your question here."
                            value={question}
                        />
                        {!loading &&
                            <SendButton onClick={() => handleQuestion(question)}/>
                        }
                    </div>

                }
            </div>


        </div>
    );
};

export default Chat;