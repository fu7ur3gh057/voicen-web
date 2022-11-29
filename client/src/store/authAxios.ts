import axios from "axios";
import {SERVER_API, TOKEN_REFRESH_API} from "../constants/apiConstants";
import jwt_decode from "jwt-decode";
import {IAccessTokenInfo, ITokens} from "../models/IUser";
import dayjs from "dayjs";
import {setCookie} from "react-use-cookie";
import {refreshTokens} from "./reducers/user/UserSlice";
import {getParsedCookie} from "../utils/cookieUtils";
import store from "./store";

const axiosService = axios.create({
    baseURL: SERVER_API,
});

axiosService.interceptors.request.use(async request => {
    let jwtTokens;
    jwtTokens = store.getState().userReducer.tokens
    if (jwtTokens === null || jwtTokens === undefined) {
        jwtTokens = getParsedCookie('tokens') as ITokens;
    }
    // checks if we have any headers in request
    if (!request.headers) {
        throw new Error(`Expected request and request.header not exists`)
    }
    const user = jwt_decode(jwtTokens?.access!) as IAccessTokenInfo
    // Compare days and get isExpired value
    const isExpired = dayjs.unix(user?.exp).diff(dayjs()) < 1
    console.log('isExpired: ', isExpired)
    // if not expired - good!
    if (!isExpired) {
        request.headers.Authorization = `Bearer ${jwtTokens.access}`
        return request
    }
    // if expired - refresh token
    const response = await axios.post(TOKEN_REFRESH_API, {
        refresh: jwtTokens?.refresh
    });
    const data = response.data as ITokens
    // const tokenInfo = jwt_decode(data.access)
    setCookie('tokens', JSON.stringify(data));
    store.dispatch(refreshTokens(data));
    request.headers.Authorization = `Bearer ${response.data.access}`
    return request;
})

export default axiosService;
