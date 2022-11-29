// import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/dist/query/react";
// import {IProfile} from "../models/IProfile";
// import {PROFILE_API, SERVER_API} from "../constants/apiConstants";
// import {RootState} from "../store/store";
//
// export const profileAPI = createApi({
//     reducerPath: 'profileAPI',
//     baseQuery: fetchBaseQuery({
//         baseUrl: `${SERVER_API}${PROFILE_API}`,
//         prepareHeaders: (headers, {getState}) => {
//             const token = (getState() as RootState).authReducer.tokens!.access
//         }
//     }),
//     tagTypes: ['Profile'],
//     endpoints: (build) => ({
//         getProfile: build.query<IProfile, void>({
//             query: () => ({
//                 url: `/me/`,
//             }),
//             providesTags: result => ['Profile']
//         }),
//         generateAPIToken: build.mutation()
//     })
// })

export const s = ''
