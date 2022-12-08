import {createContext, useState} from "react";
import {ChildrenProps} from "../index";

export interface ILoadingContext {
    globalLoading: boolean,
    activateLoadingListener: () => void,
    deactivateLoadingListener: () => void,
}

const LoadingContext = createContext<ILoadingContext | null>(null);


const LoadingContextProvider = ({children}: ChildrenProps) => {
    const [globalLoading, setGlobalLoading] = useState(false);

    const activateLoading = () => {
    }

    const deactivateLoading = () => {

    }

    const contextData = {
        globalLoading: globalLoading,
        activateLoadingListener: activateLoading,
        deactivateLoadingListener: deactivateLoading
    } as ILoadingContext

    return (
        <LoadingContext.Provider value={contextData}>
            {children}
        </LoadingContext.Provider>
    )
}

export {LoadingContext, LoadingContextProvider}
