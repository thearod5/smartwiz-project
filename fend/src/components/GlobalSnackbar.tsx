import React from "react";
import {Alert, Snackbar} from "@mui/material";

const GlobalSnackbar: React.FC<{
    message: string;
    severity: "success" | "error" | "info" | "warning"; open: boolean; onClose: () => void
}> = ({
          message,
          severity,
          open,
          onClose,
      }) => (
    <Snackbar open={open} autoHideDuration={6000} onClose={onClose}>
        <Alert onClose={onClose} severity={severity} sx={{width: "100%"}}>
            {message}
        </Alert>
    </Snackbar>
);

export default GlobalSnackbar;
