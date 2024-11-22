import axios from "axios";
import useAuthState from "../states/authState";
import {useSnackbarState} from "../states/snackbarState";

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

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        const {setSnackbar} = useSnackbarState.getState();

        if (error.response) {
            // Extract the failed endpoint and the error message
            const endpoint = error.config?.url || "Unknown endpoint";
            const status = error.response?.status;
            const errorMessage =
                error.response?.data?.message || error.message || "An error occurred";

            // Set the snackbar with detailed error info
            setSnackbar(
                `Request to ${endpoint} failed with status ${status}: ${errorMessage}`,
                "error"
            );
        } else {
            // Handle network errors or server unavailability
            setSnackbar(
                `Network error while attempting to reach ${
                    error.config?.url || "Unknown endpoint"
                }: ${error.message || "Unknown error"}`,
                "error"
            );
        }

        return Promise.reject(error);
    }
);

export default apiClient;
