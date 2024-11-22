import apiClient from "./api";
import useAuthState from "../states/authState";

export const createAccount = async (
    email: string,
    firstName: string,
    lastName: string,
    password: string
) => {
    const response = await apiClient.post("/account", {
        email,
        firstName,
        lastName,
        password,
    });
    return response.data;
};

export const login = async (email: string, password: string) => {
    const response = await apiClient.post("/login", {email, password});
    const {access, refresh} = response.data;

    const setTokens = useAuthState.getState().setTokens;
    setTokens(access, refresh);

    return response.data;
};

export const refreshAccessToken = async () => {
    const {refreshToken, setTokens, clearTokens} = useAuthState.getState();
    if (!refreshToken) {
        throw new Error("No refresh token available");
    }

    try {
        const response = await apiClient.post("/refresh", {refresh: refreshToken});
        const {access} = response.data;
        setTokens(access, refreshToken);
        return access;
    } catch (error) {
        clearTokens();
        throw error;
    }
};

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            try {
                await refreshAccessToken();
                return apiClient.request(error.config);
            } catch (refreshError) {
                useAuthState.getState().clearTokens();
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);