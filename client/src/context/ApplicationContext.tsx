import {createContext, useState} from "react";
import {ChildrenProps} from "./index";

export interface IApplicationContext {
    globalLoading: boolean,
    activateLoadingListener: () => void,
    deactivateLoadingListener: () => void,
}

const ApplicationContext = createContext<IApplicationContext | null>(null);


const ApplicationContextProvider = ({children}: ChildrenProps) => {
    const [globalLoading, setGlobalLoading] = useState(false);

    const activateLoading = () => {
    }

    const deactivateLoading = () => {

    }

    const contextData = {
        globalLoading: globalLoading,
        activateLoadingListener: activateLoading,
        deactivateLoadingListener: deactivateLoading
    } as IApplicationContext

    return (
        <ApplicationContext.Provider value={contextData}>
            {children}
        </ApplicationContext.Provider>
    )
}

export {ApplicationContext, ApplicationContextProvider}
