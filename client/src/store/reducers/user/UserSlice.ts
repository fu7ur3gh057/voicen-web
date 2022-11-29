import {ITokens} from "../../../models/IUser";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {login} from "./ActionCreators";
import {IProfile} from "../../../models/IProfile";

type AuthenticationState = {
    tokens: ITokens | null,
    // profile: IProfile | null,
    isLoading: boolean,
    error: string
}

const initialState: AuthenticationState = {
    tokens: null,
    isLoading: false,
    error: ''
}

export const userSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        refreshTokens(state, action: PayloadAction<ITokens>) {
            state.tokens = action.payload;
        }
    },
    extraReducers: {
        [login.pending.type]: (state) => {
            state.isLoading = true;
        },
        [login.fulfilled.type]: (state, action: PayloadAction<ITokens>) => {
            state.isLoading = false;
            state.error = '';
            state.tokens = action.payload;
        },
        [login.rejected.type]: (state, action: PayloadAction<string>) => {
            state.isLoading = false;
            state.error = action.payload
        },
    },
})


export const {refreshTokens} = userSlice.actions;
export default userSlice.reducer;
