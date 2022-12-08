import {PlayerAction, PlayerActionType} from "./PlayerActions";

export type PlayerState = {
    isPlaying: boolean,
    isRepeating: boolean,
    progressTime: string,
    durationTime: string,
    fileUrl: string,
    fileImage: string,
}

export const initialPlayerState: PlayerState = {
    isPlaying: false,
    isRepeating: false,
    progressTime: '',
    durationTime: '',
    fileUrl: '',
    fileImage: '',
}

export const PlayerReducer = (state: PlayerState, action: PlayerAction): PlayerState => {
    const {type, payload} = action;
    switch (type) {
        case PlayerActionType.SetAudioFile:
            return {...state, fileUrl: payload}
        case PlayerActionType.SetProgressTime:
            return {...state, progressTime: payload};
        case PlayerActionType.SetDurationTime:
            return {...state, durationTime: payload};
        case PlayerActionType.SetIsPlaying:
            return {...state, isPlaying: payload};
        case PlayerActionType.SetIsRepeating:
            return {...state, isRepeating: payload};
        default:
            return state
    }
}

