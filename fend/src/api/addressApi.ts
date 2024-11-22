import apiClient from "./api";

export const createAddress = async (address: string) => {
    const response = await apiClient.post("/address", { address });
    return response.data;
};