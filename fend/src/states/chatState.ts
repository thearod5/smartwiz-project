import {create} from "zustand";
import mockChatHistory from "./chat_history.json"; // Import mock chat history

interface ChatState {
    messages: { role: string; content: string }[];
    useMockData: boolean; // New flag to toggle mock data
    addMessage: (message: { role: string; content: string }) => void;
    clearMessages: () => void;
    initializeMessages: () => void; // Initialize messages with mock or empty state
    toggleMockData: () => void; // Toggle mock data on or off
}

const useChatStore = create<ChatState>((set, get) => ({
    messages: [],
    useMockData: false, // Default to using mock data

    addMessage: (message) =>
        set((state) => ({messages: [...state.messages, message]})),

    clearMessages: () => set({messages: []}),

    initializeMessages: () => {
        const {useMockData} = get(); // Access the current mock data flag
        if (useMockData) {
            set({messages: mockChatHistory.messages}); // Load mock data
        } else {
            set({messages: []}); // Clear messages if not using mock data
        }
    },

    toggleMockData: () =>
        set((state) => {
            const newUseMockData = !state.useMockData;
            return {useMockData: newUseMockData, messages: []}; // Reset messages on toggle
        }),
}));

export default useChatStore;
