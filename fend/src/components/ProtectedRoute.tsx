import React from "react";
import {Navigate, useLocation} from "react-router-dom";
import useAuthState from "../states/authState";

interface ProtectedRouteProps {
    children: JSX.Element;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({children}) => {
    const {accessToken} = useAuthState();
    const location = useLocation(); // Capture the current location

    if (!accessToken) {
        // Redirect to login or home page, saving the current path in state
        return <Navigate to="/" state={{from: location}}/>;
    }

    return children;
};

export default ProtectedRoute;
