import axios from "axios";
import useAuthState from "../states/authState";

const API_BASE_URL = "http://localhost:3000";

const apiClient = axios.create({
    baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use(
    (config) => {
        const {accessToken} = useAuthState.getState();
        if (accessToken && config.headers) {
            config.headers["Authorization"] = `Bearer ${accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default apiClient;
