import {createContext, useEffect, useState} from "react";
import useCookie from "react-use-cookie";
import {ChildrenProps} from "../index";

export enum ThemeTypes {
    DARK_THEME = 'DARK',
    LIGHT_THEME = 'LIGHT',
}

export type Theme = {
    value: string
}

export interface IThemeContext {
    onChangeListener: () => string
    theme: string
}

const ThemeContext = createContext<IThemeContext | null>(null);

const ThemeContextProvider = ({children}: ChildrenProps) => {
    const cookieName = 'theme';
    const [themeCookie, setThemeCookie] = useCookie(cookieName, ThemeTypes.LIGHT_THEME);
    const [themeValue, setThemeValue] = useState<string>(themeCookie);

    const setThemeListener = () => {
        if (themeCookie === ThemeTypes.LIGHT_THEME) {
            setThemeValue(ThemeTypes.DARK_THEME);
            setThemeCookie(ThemeTypes.DARK_THEME);
        } else {
            setThemeValue(ThemeTypes.LIGHT_THEME);
            setThemeCookie(ThemeTypes.LIGHT_THEME);
        }
    }

    const contextData = {
        theme: themeValue,
        onChangeListener: setThemeListener
    } as IThemeContext;
    return (
        <ThemeContext.Provider value={contextData}>
            {children}
        </ThemeContext.Provider>
    )
}

export {ThemeContext, ThemeContextProvider};
