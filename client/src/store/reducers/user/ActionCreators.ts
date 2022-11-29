import {createAsyncThunk} from "@reduxjs/toolkit";
import {getCookie, setCookie} from "react-use-cookie";
import {ITokens} from "../../../models/IUser";
import axios from "axios";
import {GET_PROFILE_API, LOGIN_API, LOGOUT_API} from "../../../constants/apiConstants";
import {getProfile} from "../profile/ActionCreators";
import authAxios from "../../authAxios";
import {refreshProfile} from "../profile/ProfileSlice";
import {IProfile} from "../../../models/IProfile";
import {getParsedCookie} from "../../../utils/cookieUtils";

type LoginProps = {
    email: string,
    password: string,
}

export const login = createAsyncThunk(
    "user/login",
    async ({email, password}: LoginProps, thunkAPI) => {
        try {
            const response = await axios.post(LOGIN_API, {
                email: email,
                password: password
            });
            const data = response.data as ITokens;
            setCookie('tokens', JSON.stringify(data));
            console.log('send profile axios');
            console.log(getParsedCookie('tokens'))
            // const profileResponse = await authAxios.get(GET_PROFILE_API);
            // const profile = profileResponse.data as IProfile
            // thunkAPI.dispatch(refreshProfile(profile));
            return data;
        } catch (e) {
            return thunkAPI.rejectWithValue("Server Error")
        }
    }
)

export const logout = createAsyncThunk(
    "user/logout",
    async (_, thunkAPI) => {
        try {
            let cookieTokens = getCookie('tokens', '');
            if (cookieTokens !== '') {
                const tokens = JSON.parse(cookieTokens) as ITokens;
                console.log(tokens?.access)
                const response = await axios.post(LOGOUT_API, {
                    refresh_token: tokens?.refresh
                }, {
                    headers: {
                        Authorization: `Bearer ${tokens?.access}`
                    }
                });
                setCookie('tokens', '')
                return response.status === 200;
            }
        } catch (e) {
            console.log(e)
            return thunkAPI.rejectWithValue(`${e}`);
        }
    }
)
