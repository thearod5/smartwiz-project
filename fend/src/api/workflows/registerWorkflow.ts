import apiClient from "../api";
import {login} from "../authApi";
import useChatStore from "../../states/chatState";


export const createAccountWorkflow = async (userData: {
    email: string;
    firstName: string;
    lastName: string;
    password: string;
    address: string;
}) => {
    const {addMessage} = useChatStore.getState();

    try {
        // Step 1: Create account
        const accountResponse = await apiClient.post("/account", {
            email: userData.email,
            firstName: userData.firstName,
            lastName: userData.lastName,
            password: userData.password,
        });

        const {id: userId} = accountResponse.data;

        // Login
        await login(userData.email, userData.password)

        // Step 2: Create address
        const addressResponse = await apiClient.post("/address", {
            address: userData.address,
        });

        const {id: addressId} = addressResponse.data;

        // Step 3: Update user's primary address
        await apiClient.put(`/account`, {
            primaryAddress: addressId,
        });

        // Step 5: Start chat
        const chatResponse = await apiClient.post("/chat", {
            messages: []
        })
        const {form, response} = chatResponse.data

        addMessage({
            role: "assistant",
            content: response
        })


    } catch (error) {
        console.error("Workflow failed:", error);
        throw error;
    }
};
