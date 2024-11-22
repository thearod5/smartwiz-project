import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {useAppState} from "../states/appState";

const LoadingMascots: React.FC = () => {
    const loading = useAppState((state) => state.loading);

    return (
        <AnimatePresence>
            {loading && (
                <motion.div
                    key="mascot"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100vw",
                        height: "100vh",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        zIndex: 9999,
                    }}
                >
                    <motion.img
                        src="/logo.png" // Replace with your mascot image path
                        alt="Loading Mascot"
                        initial={{ scale: 1 }}
                        animate={{ scale: [1, 1.1, 1] }}
                        transition={{
                            repeat: Infinity,
                            duration: 1.5,
                        }}
                        style={{
                            width: "150px",
                            height: "150px",
                            borderRadius: "50%",
                        }}
                    />
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default LoadingMascots;
