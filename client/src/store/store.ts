import {combineReducers, configureStore} from "@reduxjs/toolkit";
import userReducer from "./reducers/user/UserSlice";
import profileReducer from "./reducers/profile/ProfileSlice";

const rootReducer = combineReducers({
    userReducer,
    profileReducer,
});

const store = configureStore({
    reducer: rootReducer
})

// export const setupStore = () => {
//     return configureStore({
//         reducer: rootReducer
//     })
// }


export type RootState = ReturnType<typeof rootReducer>;
// export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = typeof store.dispatch;

export default store;
