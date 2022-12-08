import {PlayerAction} from "./PlayerActions";
import React, {createContext, useEffect, useReducer} from "react";
import {initialPlayerState, PlayerReducer, PlayerState} from "./PlayerReducer";
import {ChildrenProps} from "../index";

export interface IPlayerContext {
    state: PlayerState,
    dispatch: React.Dispatch<PlayerAction>
}

const PlayerContext = createContext<IPlayerContext | null>(null);

const PlayerContextProvider = ({children}: ChildrenProps) => {
    const [state, dispatch] = useReducer(PlayerReducer, initialPlayerState);

    useEffect(() => {

    }, [])

    const contextData = {
        state: state,
        dispatch: dispatch,
    } as IPlayerContext
    return (
        <PlayerContext.Provider value={contextData}>
            {children}
        </PlayerContext.Provider>
    )
}

export {PlayerContext, PlayerContextProvider};
