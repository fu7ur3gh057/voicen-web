import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Application from './app/Application';
import {BrowserRouter} from "react-router-dom";
import {LoadingContextProvider} from "./context/loading/LoadingContext";
import {AuthContextProvider} from "./context/auth/AuthContext";
import {PlayerContextProvider} from "./context/player/PlayerContext";
import {ThemeContextProvider} from "./context/theme/ThemeContext";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <BrowserRouter>
        <ThemeContextProvider>
            <LoadingContextProvider>
                <AuthContextProvider>
                    <PlayerContextProvider>
                        <Application/>
                    </PlayerContextProvider>
                </AuthContextProvider>
            </LoadingContextProvider>
        </ThemeContextProvider>
    </BrowserRouter>
);
