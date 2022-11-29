import {IProfile} from "../../../models/IProfile";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {getProfile} from "./ActionCreators";

type ProfileProps = {
    profile: IProfile | null,
    isLoading: boolean,
    error: string,
}

const initialState: ProfileProps = {
    profile: null,
    isLoading: false,
    error: ''
}

const profileSlice = createSlice({
    name: 'profile',
    initialState,
    reducers: {
        refreshProfile(state, action: PayloadAction<IProfile>) {
            state.profile = action.payload
        }
    },
    extraReducers: {
        [getProfile.pending.type]: (state) => {
            state.isLoading = true;
        },
        [getProfile.fulfilled.type]: (state, action: PayloadAction<IProfile>) => {
            state.isLoading = false;
            state.error = '';
            state.profile = action.payload;
        },
        [getProfile.rejected.type]: (state, action: PayloadAction<string>) => {
            state.isLoading = false;
            state.error = action.payload
        },
    }
})

export const {refreshProfile} = profileSlice.actions
export default profileSlice.reducer;
