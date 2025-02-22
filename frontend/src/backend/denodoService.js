export const streamAnswerQuestion = async (question) => {
    const params = new URLSearchParams({
        question,
        plot: false,
        embeddings_provider: "googleaistudio",
        embeddings_model: "models/text-embedding-004",
        vector_store_provider: "Chroma",
        sql_gen_provider: "googleaistudio",
        sql_gen_model: "gemini-1.5-flash",
        chat_provider: "googleaistudio",
        chat_model: "gemini-1.5-flash",
        vdp_database_names: "samples_bank",
        expand_set_views: true,
        markdown_response: true,
        vector_search_k: 5,
        mode: "default",
        disclaimer: true,
        verbose: true
    }).toString();

    const credentials = btoa("admin:admin");

    try {
        const response = await fetch(`http://localhost:8008/streamAnswerQuestion?${params}`, {
            method: 'GET',
            headers: {
                "Accept": "*/*",
                "Authorization": `Basic ${credentials}`
            }
        });

        const textResponse = await response.text();

        return textResponse;

    } catch (error) {
        throw error;
    }
};

export const answerQuestion = async (question) => {
    const params = new URLSearchParams({
        question,
        plot: false,
        embeddings_provider: "googleaistudio",
        embeddings_model: "models/text-embedding-004",
        vector_store_provider: "Chroma",
        sql_gen_provider: "googleaistudio",
        sql_gen_model: "gemini-1.5-flash",
        chat_provider: "googleaistudio",
        chat_model: "gemini-1.5-flash",
        vdp_database_names: "samples_bank",
        expand_set_views: true,
        markdown_response: true,
        vector_search_k: 5,
        mode: "default",
        disclaimer: true,
        verbose: true
    }).toString();

    const credentials = btoa("admin:admin");

    try {
        const response = await fetch(`http://localhost:8008/answerQuestion?${params}`, {
            method: 'GET',
            headers: {
                "Accept": "application/json",
                "Authorization": `Basic ${credentials}`
            }
        });

        const jsonResponse = await response.json();

        const answer = jsonResponse.answer;

        return answer;

    } catch (error) {
        throw error;
    }
};