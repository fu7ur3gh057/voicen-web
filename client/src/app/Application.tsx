import React, {useContext, useEffect, useReducer, useState} from 'react';
import {useAuthAxios} from "../hooks/useAuthAxios";
import {ITranscribe} from "../models/ITranscribe";
import {IProfile} from "../models/IProfile";
import {initialPlayerState, PlayerReducer} from "../context/player/PlayerReducer";
import {PlayerActionType} from "../context/player/PlayerActions";
import TestComp from "../ui/components/TestComp";
import {AuthContext} from "../context/auth/AuthContext";
import {PlayerContext} from "../context/player/PlayerContext";
import WavePlayer from "../ui/components/wavePlayer/WavePlayer";

function Application() {
    const authContext = useContext(AuthContext);
    const playerContext = useContext(PlayerContext);
    const {state, dispatch} = playerContext!;
    // const [state, dispatch] = useReducer(PlayerReducer, initialPlayerState);

    const [transcribeList, setTranscribeList] = useState<ITranscribe[]>([]);
    const auth = useAuthAxios();
    const [profile, setProfile] = useState<IProfile | null | undefined>(null)

    useEffect(() => {
        setProfile(authContext?.profile)
        dispatch({type: PlayerActionType.SetProgressTime, payload: '00:01:45'})
        dispatch({type: PlayerActionType.SetAudioFile, payload: '30fdcf7d-b8b8-4c2c-a1e6-718ffd5cfe53'})
    }, [authContext?.profile])

    const getProfile = async () => {

    }

    const getTranscribeList = async () => {

    }

    const addName = () => {
        dispatch({type: PlayerActionType.SetAudioFile, payload: '30fdcf7d-b8b8-4c2c-a1e6-718ffd5cfe53'})
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
                <p>{state.fileUrl}</p>
            </div>
            <button onClick={() => addName()}>add name</button>
            <TestComp/>
            <WavePlayer/>
        </div>
    );
}

export default Application;
