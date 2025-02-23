export const answerQuestion = async (chatId, question) => {
    try {
        const response = await fetch(`http://localhost:5000/send`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                chat_id: chatId,
                message: question
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const jsonResponse = await response.json();

        // Extraemos la respuesta del backend
        const answer = jsonResponse.respuesta;

        return answer;
    } catch (error) {
        throw error;
    }
};


export const getChatHistory = async (chatId) => {
    try {
        const response = await fetch(`http://localhost:5000/history/${chatId}`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            const errorText = await response.text(); // Captura el mensaje de error si lo hay
            throw new Error(`Error HTTP ${response.status}: ${errorText}`);
        }

        const jsonResponse = await response.json();
        return jsonResponse.mensajes; // ✅ Devolvemos solo la lista de mensajes
    } catch (error) {
        console.error("Error en la petición:", error);
        throw error;
    }
};

export const getChatIds = async () => {
    try {
        const response = await fetch(`http://localhost:5000/chats`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Error HTTP ${response.status}: ${errorText}`);
        }

        const jsonResponse = await response.json();
        return jsonResponse.chats;
    } catch (error) {
        console.error("Error en la petición:", error);
        throw error;
    }
}