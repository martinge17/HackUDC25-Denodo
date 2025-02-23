// export const answerQuestion = async (question) => {
//     const params = new URLSearchParams({
//         question,
//         plot: false,
//         embeddings_provider: "googleaistudio",
//         embeddings_model: "models/text-embedding-004",
//         vector_store_provider: "Chroma",
//         sql_gen_provider: "googleaistudio",
//         sql_gen_model: "gemini-1.5-flash",
//         chat_provider: "googleaistudio",
//         chat_model: "gemini-1.5-flash",
//         vdp_database_names: "samples_bank",
//         expand_set_views: true,
//         markdown_response: true,
//         vector_search_k: 5,
//         mode: "default",
//         disclaimer: true,
//         verbose: true
//     }).toString();
//
//     const credentials = btoa("admin:admin");
//
//     try {
//         const response = await fetch(`http://localhost:8008/answerQuestion?${params}`, {
//             method: 'GET',
//             headers: {
//                 "Accept": "application/json",
//                 "Authorization": `Basic ${credentials}`
//             }
//         });
//
//         const jsonResponse = await response.json();
//
//         const answer = jsonResponse.answer;
//
//         return answer;
//
//     } catch (error) {
//         throw error;
//     }
// };

export const answerQuestion = async (chatId, question) => {
    try {
        const response = await fetch(`http://100.86.28.10:8888/send`, {
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
        const response = await fetch(`http://100.86.28.10:8888/history/${chatId}`, {
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
        const response = await fetch(`http://100.86.28.10:8888/chats`, {
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
};