import {getCookie} from "react-use-cookie";

export const getParsedCookie = (name: string) => {
    try {
        return JSON.parse(getCookie(name));
    } catch (e) {
        return null;
    }
}
