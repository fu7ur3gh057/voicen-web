import React, {useContext, useEffect, useReducer, useState} from 'react';
import {useAuthAxios} from "../hooks/useAuthAxios";
import {GET_TRANSCRIBE_LIST_API} from "../constants/apiConstants";
import {ITranscribe} from "../models/ITranscribe";
import {IPaginate} from "../models/IPaginate";
import {getCookie} from "react-use-cookie";
import AuthContext from "../context/auth/AuthContext";
import {IProfile} from "../models/IProfile";
import {initialPlayerState, PlayerReducer} from "../reducers/player/PlayerReducer";
import {PlayerActionType} from "../reducers/player/PlayerActions";

function Application() {
    const authContext = useContext(AuthContext);
    const [state, dispatch] = useReducer(PlayerReducer, initialPlayerState);

    const [transcribeList, setTranscribeList] = useState<ITranscribe[]>([]);
    const auth = useAuthAxios();
    const [profile, setProfile] = useState<IProfile | null | undefined>(null)

    useEffect(() => {
        setProfile(authContext?.profile)
        dispatch({type: PlayerActionType.SetAudioFile, payload: 'lol.mp3'})
        dispatch({type: PlayerActionType.SetProgressTime, payload: '00:01:45'})
    }, [authContext?.profile])

    const getProfile = async () => {

    }

    const getTranscribeList = async () => {

    }

    const loginClickListener = () => {
        authContext?.loginListener('fu7ur3gh057@gmail.com', 'lol123lol')
    }

    return (
        <div>
            <button onClick={() => loginClickListener()}>Login</button>
            <h1>JWT ACCESS TOKEN {authContext?.profile?.email}</h1>
            <div style={{display: "flex", gap: "20px"}}>
                <p>{state.progressTime}</p>
                <p>{state.fileName}</p>
            </div>
            <button></button>
        </div>
    );
}

export default Application;
