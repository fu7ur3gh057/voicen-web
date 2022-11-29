import {createAsyncThunk} from "@reduxjs/toolkit";
import {GET_PROFILE_API} from "../../../constants/apiConstants";
import {IProfile} from "../../../models/IProfile";
import authAxios from "../../authAxios";

export const getProfile = createAsyncThunk(
    "profile/me",
    async (_, thunkAPI) => {
        try {

        } catch (e) {
            console.log(e)
        }
    }
)

export const updateProfile = createAsyncThunk(
    "profile/update",
    async (_, thunkAPI) => {

    }
)

export const generateAPIToken = createAsyncThunk(
    "profile/generateAPIToken",
    async (_, thunkAPI) => {

    }
)
