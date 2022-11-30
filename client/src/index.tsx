import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Application from './app/Application';
import {BrowserRouter} from "react-router-dom";
import {ApplicationContextProvider} from "./context/ApplicationContext";
import {AuthContextProvider} from "./context/auth/AuthContext";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <BrowserRouter>
        <ApplicationContextProvider>
            <AuthContextProvider>
                <Application/>
            </AuthContextProvider>
        </ApplicationContextProvider>
    </BrowserRouter>
);
