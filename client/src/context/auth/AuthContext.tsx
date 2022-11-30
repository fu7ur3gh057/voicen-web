import React, {createContext, useEffect, useState} from 'react';
import {ITokens} from "../../models/IAuth";
import {IProfile} from "../../models/IProfile";
import useCookie from 'react-use-cookie';
import {useAuthAxios} from "../../hooks/useAuthAxios";
import {GET_PROFILE_API, LOGIN_API} from "../../constants/apiConstants";
import axios from "axios";
import {ChildrenProps} from "../index";

export interface IAuthContext {
    tokens: ITokens | null,
    profile: IProfile | null,
    isLoading: boolean,
    // Listeners
    loginListener: (email: string, password: string) => void,
    logoutListener: () => void,
    getProfileListener: () => void,
}

const AuthContext = createContext<IAuthContext | null>(null);
export default AuthContext;

const getTokensCookie = (cookie: string) => {
    if (cookie !== '') return JSON.parse(cookie) as ITokens;
    else return null;
}

const AuthContextProvider = ({children}: ChildrenProps) => {
    const [tokensCookie, setTokensCookie] = useCookie('tokens', '');
    const [tokens, setTokens] = useState<ITokens | null>(getTokensCookie(tokensCookie));
    const [profile, setProfile] = useState<IProfile | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const authAxios = useAuthAxios();

    // Init Effect
    useEffect(() => {
        if (tokens !== null) {
            fetchProfile();
        }
    }, [])

    // Cookie Tokens Effect
    useEffect(() => {
        if (tokensCookie !== '') {
            const parsedTokens = JSON.parse(tokensCookie);
            setTokens(parsedTokens);
            console.log(`set tokens ${parsedTokens}`)
        } else {
            setTokens(null);
            setProfile(null)
        }
    }, [tokensCookie])

    const fetchProfile = async () => {
        const response = await authAxios.get(GET_PROFILE_API);
        const data = response.data as IProfile;
        setProfile(data);
        console.log(`set profile ${data}`)
    }

    // Listeners
    const loginCallback = async (email: string, password: string) => {
        const response = await axios.post(LOGIN_API, {email: email, password: password});
        const data = response.data as ITokens;
        setTokensCookie(JSON.stringify(data));
    }

    const logoutCallback = () => {
        setTokensCookie('');
    }

    const getProfileCallback = () => {

    }

    const contextData = {
        tokens: tokens,
        profile: profile,
        isLoading: isLoading,
        loginListener: loginCallback,
        logoutListener: logoutCallback,
        getProfileListener: getProfileCallback,
    } as IAuthContext;

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};

export {AuthContextProvider};
