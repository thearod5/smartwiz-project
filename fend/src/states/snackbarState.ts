import {create} from "zustand";

interface SnackbarState {
    message: string;
    severity: "success" | "error" | "info" | "warning";
    open: boolean;
    setSnackbar: (message: string, severity: "success" | "error" | "info" | "warning") => void;
    closeSnackbar: () => void;
}

export const useSnackbarState = create<SnackbarState>((set) => ({
    message: "",
    severity: "info",
    open: false,
    setSnackbar: (message, severity) => set({message, severity, open: true}),
    closeSnackbar: () => set({open: false}),
}));
