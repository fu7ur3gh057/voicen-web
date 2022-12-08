export enum PlayerActionType {
    SetAudioFile,
    SetProgressTime,
    SetDurationTime,
    SetIsPlaying,
    SetIsRepeating,
}

export interface SetAudioFileActionType {
    type: PlayerActionType.SetAudioFile,
    payload: string
}

export interface SetProgressTimeActionType {
    type: PlayerActionType.SetProgressTime,
    payload: string,
}

export interface SetDurationTimeActionType {
    type: PlayerActionType.SetDurationTime,
    payload: string,
}

export interface SetIsPlayingActionType {
    type: PlayerActionType.SetIsPlaying,
    payload: boolean,
}

export interface SetIsRepeatingActionType {
    type: PlayerActionType.SetIsRepeating,
    payload: boolean,
}

export type PlayerAction =
    SetAudioFileActionType
    | SetProgressTimeActionType
    | SetDurationTimeActionType
    | SetIsPlayingActionType
    | SetIsRepeatingActionType
