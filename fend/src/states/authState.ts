import {create} from "zustand";

interface AuthState {
    accessToken: string | null;
    refreshToken: string | null;
    setTokens: (accessToken: string, refreshToken: string) => void;
    clearTokens: () => void;
}

const useAuthState = create<AuthState>((set) => ({
    accessToken: null,
    refreshToken: null,
    setTokens: (accessToken, refreshToken) =>
        set({accessToken, refreshToken}),
    clearTokens: () => set({accessToken: null, refreshToken: null}),
}));

export default useAuthState;
