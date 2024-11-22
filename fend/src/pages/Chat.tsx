import React, {useEffect, useRef, useState} from "react";
import {
    Box,
    Button,
    CircularProgress,
    List,
    ListItem,
    ListItemText,
    Paper,
    TextField,
    Typography,
} from "@mui/material";
import useChatStore from "../states/chatState";
import apiClient from "../api/api";
import {useNavigate} from "react-router-dom";
import {useAppState} from "../states/appState";
import useFormState from "../states/formState";

const ChatPage: React.FC = () => {

    const {messages, addMessage, clearMessages, initializeMessages} = useChatStore();
    const [input, setInput] = useState("");
    const [typing, setTyping] = useState(false);
    const initialMessageSent = useRef(false);
    const {setLoading} = useAppState.getState();
    const {setTaxItems, setSalary} = useFormState.getState();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchInitialMessage = async () => {
            if (!initialMessageSent.current && messages.length === 0) {
                initialMessageSent.current = true
                setLoading(true); // Show loading spinner
                apiClient.post("/chat", {messages: []}).then((chatResponse) => {
                    const {response} = chatResponse.data;
                    addMessage({role: "assistant", content: response});
                    setLoading(false); // Hide loading spinner
                })

            }
        };

        fetchInitialMessage();
    }, [messages]);

    const handleSendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = {role: "user", content: input};
        addMessage(userMessage);

        setInput("");
        setTyping(true); // Show loading spinner


        try {
            const sendMessages = [...messages, userMessage]
            apiClient.post("/chat", {messages: sendMessages}).then((chatResponse) => {
                const {response, form} = chatResponse.data;

                if (form) {
                    console.log("Tax Items:", form)
                    setTaxItems(form.items)
                    setSalary(form.salary)
                    setLoading(true)
                    navigate("/form")
                    setLoading(false)
                } else {
                    addMessage({role: "assistant", content: response});
                }
            })

        } catch (error) {
            console.error("Error fetching chat response:", error);
            addMessage({
                role: "assistant",
                content: "Sorry, something went wrong. Please try again.",
            });
        } finally {
            setTyping(false); // Hide loading spinner
        }
    };

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                alignItems: "center",
                minHeight: "90vh",
                padding: 2,
                gap: 2,
            }}
        >
            <Typography variant="h4">Chat with AI Agent</Typography>
            <Paper
                elevation={3}
                sx={{
                    width: "100%",
                    maxWidth: 600,
                    flexGrow: 1,
                    padding: 2,
                    overflowY: "auto",
                }}
            >
                <List>
                    {messages.map((msg, index) => (
                        <ListItem
                            key={index}
                            sx={{
                                justifyContent:
                                    msg.role === "user" ? "flex-end" : "flex-start",
                            }}
                        >
                            <ListItemText
                                primary={msg.content}
                                sx={{
                                    textAlign: msg.role === "user" ? "right" : "left",
                                    backgroundColor:
                                        msg.role === "user" ? "primary.light" : "grey.300",
                                    borderRadius: 2,
                                    padding: 1,
                                    maxWidth: "75%",
                                }}
                            />
                        </ListItem>
                    ))}
                    {typing && (
                        <ListItem sx={{justifyContent: "flex-start"}}>
                            <ListItemText
                                primary={
                                    <Box
                                        sx={{
                                            display: "flex",
                                            alignItems: "center",
                                            gap: 1,
                                        }}
                                    >
                                        <CircularProgress size={16}/>
                                        <Typography variant="body2">AI is typing...</Typography>
                                    </Box>
                                }
                            />
                        </ListItem>
                    )}
                </List>
            </Paper>
            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    width: "100%",
                    maxWidth: 600,
                }}
            >
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    disabled={typing} // Disable input while loading
                    multiline // Enable multiline
                    maxRows={4} // Limit to 4 rows, or remove for unlimited
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSendMessage}
                    disabled={typing} // Disable send button while loading
                >
                    Send
                </Button>
                <Button variant="outlined" color="secondary" onClick={clearMessages}>
                    Clear
                </Button>
            </Box>
        </Box>
    );
};

export default ChatPage;
