import React, {useState} from "react";
import {Box, Button, Link, TextField, Typography} from "@mui/material";
import {useLocation, useNavigate} from "react-router-dom";
import {login} from "../api/authApi";
import {useAppState} from "../states/appState";

const Home: React.FC = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [emailError, setEmailError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    const {setLoading} = useAppState.getState();
    const location = useLocation();

    const handleLogin = async () => {
        // Reset errors
        setEmailError(false);
        setPasswordError(false);

        let valid = true;

        if (!email.trim()) {
            setEmailError(true);
            valid = false;
        }

        if (!password.trim()) {
            setPasswordError(true);
            valid = false;
        }

        if (!valid) {
            return;
        }

        setLoading(true);
        login(email, password)
            .then(() => {
                const from = location.state?.from?.pathname || "/chat";
                navigate(from, {replace: true});
            })
            .catch((e) => console.error(e))
            .finally(() => setLoading(false));
    };

    const handleRegisterNavigate = () => {
        navigate("/register");
    };

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
                padding: 2,
            }}
        >
            <Typography variant="h4" gutterBottom>
                Login
            </Typography>
            <Box
                component="form"
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    gap: 2,
                    width: "100%",
                    maxWidth: 400,
                }}
                noValidate
                autoComplete="off"
            >
                <TextField
                    label="Email"
                    variant="outlined"
                    fullWidth
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    error={emailError}
                    helperText={emailError ? "Email is required" : ""}
                />
                <TextField
                    label="Password"
                    type="password"
                    variant="outlined"
                    fullWidth
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    error={passwordError}
                    helperText={passwordError ? "Password is required" : ""}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleLogin}
                    fullWidth
                >
                    Login
                </Button>
            </Box>
            <Typography sx={{marginTop: 2}}>
                Don't have an account?{" "}
                <Link
                    component="button"
                    variant="body2"
                    onClick={handleRegisterNavigate}
                >
                    Register
                </Link>
            </Typography>
        </Box>
    );
};

export default Home;
