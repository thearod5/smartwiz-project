import React from "react";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import {ROUTES} from "./routes";
import {ThemeProvider} from "@mui/material/styles";
import theme from "./theme";
import LoadingMascots from "./components/LoadingMascots";
import Chat from "./pages/Chat";
import TaxForm from "./pages/Form";
import Summary from "./pages/Summary";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import Receipt from "./pages/Receipt"; // Import ProtectedRoute

const App: React.FC = () => {
    return (
        <Router>
            <ThemeProvider theme={theme}>
                <LoadingMascots/>
                <Routes>
                    <Route path={ROUTES.HOME} element={<Home/>}/>
                    <Route path={ROUTES.REGISTER} element={<Register/>}/>

                    {/* Protected Routes */}
                    <Route
                        path={ROUTES.CHAT}
                        element={
                            <ProtectedRoute>
                                <Chat/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path={ROUTES.FORM}
                        element={
                            <ProtectedRoute>
                                <TaxForm/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path={ROUTES.SUMMARY}
                        element={
                            <ProtectedRoute>
                                <Summary/>
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path={ROUTES.RECEIPT}
                        element={
                            <ProtectedRoute>
                                <Receipt/>
                            </ProtectedRoute>
                        }
                    />


                    <Route path="*" element={<NotFound/>}/> {/* Catch-all route */}
                </Routes>
            </ThemeProvider>
        </Router>
    );
};

export default App;
