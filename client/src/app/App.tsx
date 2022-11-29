import React, {useState} from 'react';
import {useAuthAxios} from "../hooks/useAuthAxios";
import {login} from "../store/reducers/user/ActionCreators";
import {GET_PROFILE_API, GET_TRANSACTION_LIST_API, GET_TRANSCRIBE_LIST_API} from "../constants/apiConstants";
import {useAppDispatch} from "../hooks/useAppDispatch";
import {useAppSelector} from "../hooks/useAppSelector";
import authAxios from "../store/authAxios";
import {ITranscribe} from "../models/ITranscribe";
import {IPaginate} from "../models/IPaginate";
import {getParsedCookie} from "../utils/cookieUtils";
import {ITokens} from "../models/IUser";
import {getCookie} from "react-use-cookie";
import {refreshTokens} from "../store/reducers/user/UserSlice";
import {refreshProfile} from "../store/reducers/profile/ProfileSlice";

function App() {
    const dispatch = useAppDispatch();
    const {tokens, isLoading, error} = useAppSelector(state => state.userReducer);
    const {profile} = useAppSelector(state => state.profileReducer);
    const [transcribeList, setTranscribeList] = useState<ITranscribe[]>([]);
    const auth = useAuthAxios();

    const getProfile = async () => {
        const response = await authAxios.get(GET_PROFILE_API);
        const data = response.data
        console.log(`profile is ${JSON.stringify(data)}`)
    }

    const getTranscribeList = async () => {
        const tokens = JSON.parse(getCookie('tokens'))
        const response = await auth.get(GET_TRANSCRIBE_LIST_API);
        const data = response.data as IPaginate<ITranscribe>
        setTranscribeList(data.results)
    }

    const loginClickListener = () => {
        dispatch(login({email: 'fu7ur3gh057@gmail.com', password: 'lol123lol'}))
    }

    return (
        <div className="App">
            {isLoading && <h1>Loading...</h1>}
            {error && <h1>{error}</h1>}
            <button onClick={() => loginClickListener()}>login</button>
            {tokens && <h1>USER {tokens?.access}</h1>}
            {profile && <h1>PROFILE {profile.email}</h1>}
            <button onClick={() => getProfile()}>Get Profile</button>
            <button onClick={() => getTranscribeList()}>Get Transcribe list</button>
            {transcribeList.map((item) => (
                <div key={item.id}>
                    <h3>{item.file_name}</h3>
                </div>
            ))}
        </div>
    );
}

export default App;
