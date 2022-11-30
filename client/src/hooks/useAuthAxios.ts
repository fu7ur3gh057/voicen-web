import axios from "axios";
import dayjs from "dayjs";
import jwt_decode from "jwt-decode";
import {setCookie} from "react-use-cookie";
import {SERVER_API, TOKEN_REFRESH_API} from "../constants/apiConstants";
import {getParsedCookie} from "../utils/cookieUtils";
import {IAccessTokenInfo, ITokens} from "../models/IAuth";


const useAuthAxios = () => {
    // getting user tokens
    const jwtTokens = getParsedCookie('tokens');
    const axiosInstance = axios.create({
        baseURL: SERVER_API,
        headers: {Authorization: `Bearer ${jwtTokens?.access}`}
    });
    // Setup Interceptor Request
    axiosInstance.interceptors.request.use(async request => {

        // checks if we have any headers in request
        if (!request.headers) {
            throw new Error(`Expected request and request.header not exists`)
        }
        const user = jwt_decode(jwtTokens?.access!) as IAccessTokenInfo
        // Compare days and get isExpired value
        const isExpired = dayjs.unix(user?.exp).diff(dayjs()) < 1
        console.log('isExpired: ', isExpired)
        // if not expired - good!
        if (!isExpired) return request
        // if expired - refresh token
        const response = await axios.post(TOKEN_REFRESH_API, {
            refresh: jwtTokens?.refresh
        })
        const data = response.data as ITokens
        // const tokenInfo = jwt_decode(data.access)
        setCookie('tokens', JSON.stringify(data));
        request.headers.Authorization = `Bearer ${response.data.access}`
        return request
    })
    return axiosInstance
}


export {useAuthAxios};
