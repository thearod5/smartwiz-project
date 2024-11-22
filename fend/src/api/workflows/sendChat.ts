import useChatStore from "../../states/chatState";
import apiClient from "../api";


export const sendChatMessage = async (message: string) => {
    const {messages, addMessage} = useChatStore.getState();

    // Add user's message to the store
    addMessage({role: "user", content: message});

    try {
        // Send message to API
        const response = await apiClient.post("/chat", {
            messages: [...messages, {role: "user", content: message}],
        });

        // Add AI response to the store
        const {response: aiResponse} = response.data;
        addMessage({role: "assistant", content: aiResponse});
    } catch (error) {
        console.error("Error sending message:", error);
    }
};
