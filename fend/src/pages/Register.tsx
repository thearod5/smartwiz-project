import React, {useState} from "react";
import {Box, Button, TextField, Typography} from "@mui/material";
import {createAccountWorkflow} from "../api/workflows/registerWorkflow";
import {useAppState} from "../states/appState";
import {useNavigate} from "react-router-dom";

const Register: React.FC = () => {
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        address: "",
    });

    const [errors, setErrors] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        address: "",
    });

    const {setLoading} = useAppState.getState();
    const navigate = useNavigate();

    const validateEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validatePassword = (password: string) => {
        return password.length >= 8;
    };

    const validateAddress = (address: string) => {
        // const parts = address.split(",")
        // console.log(parts)
        // return parts.length - 1 === 4
        return true;
    };

    const validateForm = () => {
        const newErrors = {
            firstName: formData.firstName ? "" : "First name is required.",
            lastName: formData.lastName ? "" : "Last name is required.",
            email: validateEmail(formData.email) ? "" : "Enter a valid email address.",
            password: validatePassword(formData.password) ? "" : "Password must be at least 8 characters.",
            address: validateAddress(formData.address) ? "" : "Enter a valid address (e.g., 123 S. Street, City, State, ZIPCODE).",
        };
        setErrors(newErrors);
        return Object.values(newErrors).every((error) => error === "");
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        setErrors((prevErrors) => ({
            ...prevErrors,
            [name]: "", // Clear error message on change
        }));
    };

    const handleRegister = async () => {
        if (!validateForm()) {
            return;
        }

        setLoading(true);
        try {
            await createAccountWorkflow(formData);
            navigate("/chat");
        } catch (error) {
            console.error("Registration failed:", error);
        } finally {
            setLoading(false);
        }
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
                Register
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
                    label="First Name"
                    name="firstName"
                    variant="outlined"
                    fullWidth
                    value={formData.firstName}
                    onChange={handleChange}
                    error={Boolean(errors.firstName)}
                    helperText={errors.firstName}
                />
                <TextField
                    label="Last Name"
                    name="lastName"
                    variant="outlined"
                    fullWidth
                    value={formData.lastName}
                    onChange={handleChange}
                    error={Boolean(errors.lastName)}
                    helperText={errors.lastName}
                />
                <TextField
                    label="Email"
                    name="email"
                    type="email"
                    variant="outlined"
                    fullWidth
                    value={formData.email}
                    onChange={handleChange}
                    error={Boolean(errors.email)}
                    helperText={errors.email}
                />
                <TextField
                    label="Password"
                    name="password"
                    type="password"
                    variant="outlined"
                    fullWidth
                    value={formData.password}
                    onChange={handleChange}
                    error={Boolean(errors.password)}
                    helperText={errors.password}
                />
                <TextField
                    label="Address"
                    name="address"
                    variant="outlined"
                    multiline
                    rows={3}
                    fullWidth
                    value={formData.address}
                    onChange={handleChange}
                    error={Boolean(errors.address)}
                    helperText={errors.address}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleRegister}
                    fullWidth
                >
                    Register
                </Button>
            </Box>
        </Box>
    );
};

export default Register;
