import React, {useContext} from 'react';
import {PlayerActionType} from "../../context/player/PlayerActions";
import {PlayerContext} from "../../context/player/PlayerContext";

const TestComp = () => {
    const playerContext = useContext(PlayerContext);
    const {state, dispatch} = playerContext!;

    return (
        <div>
            <button onClick={
                () => dispatch({type: PlayerActionType.SetAudioFile, payload: 'qaqa_lol.mp3'}
                )}>change name
            </button>
            <h1>salan</h1>
            <h1>{state.fileUrl}</h1>
        </div>
    );
};

export default TestComp;
