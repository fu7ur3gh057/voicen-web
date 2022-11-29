export const SERVER_API = 'http://127.0.0.1:8000/api/v1'

// PARENT URLS
export const AUTH_API = '/auth';
export const PROFILE_API = '/profile';
export const SYNTHESIS_API = '/synthesis';
export const TRANSCRIBE_API = '/transcribe';
export const PAYMENT_API = '/payment';
export const MONITORING_API = '/payment';
export const CHAT_API = '/payment';
export const NOTIFICATION_API = '/payment';

// AUTH
export const REGISTER = `${SERVER_API}${AUTH_API}/register/`;
// export const VERIFY_EMAIL = `${SERVER_API}${AUTH_API}/`;
export const LOGIN_API = `${SERVER_API}${AUTH_API}/login/`;
export const TOKEN_REFRESH_API = `${SERVER_API}${AUTH_API}/login/refresh/`;
export const LOGOUT_API = `${SERVER_API}${AUTH_API}/logout/`;
export const UPDATE_PASSWORD_API = `${SERVER_API}${AUTH_API}/password/update/`;
export const RESET_PASSWORD_API = `${SERVER_API}${AUTH_API}/password/reset/`;
export const SET_NEW_PASSWORD_API = `${SERVER_API}${AUTH_API}/password/new/`;
export const DELETE_USER_API = `${SERVER_API}${AUTH_API}/delete/`;

// PROFILE
export const GET_PROFILE_API = `${SERVER_API}${PROFILE_API}/me/`;
export const UPDATE_PROFILE_API = `${SERVER_API}${PROFILE_API}/update/`;
export const GENERATE_API_TOKEN_API = `${SERVER_API}${PROFILE_API}/api-token/`;

// PAYMENT
export const GET_WALLET_API = `${SERVER_API}${PAYMENT_API}/wallet/`;
export const CREATE_TRANSACTION_API = `${SERVER_API}${PAYMENT_API}/transaction/create/`;
export const RECEIVE_TRANSACTION_API = `${SERVER_API}${PAYMENT_API}/transaction/receive/`;
export const GET_TRANSACTION_LIST_API = `${SERVER_API}${PAYMENT_API}/transaction/`;
export const GET_SUBSCRIPTION_LIST_API = `${SERVER_API}${PAYMENT_API}/subscription/`;
export const CREATE_SUBSCRIPTION_API = `${SERVER_API}${PAYMENT_API}/subscription/create/`;
export const CANCEL_SUBSCRIPTION_API = `${SERVER_API}${PAYMENT_API}/subscription/cancel/`;
export const GET_OPERATION_LIST_API = `${SERVER_API}${PAYMENT_API}/operation/`;

// TRANSCRIBE
export const GET_TRANSCRIBE_LIST_API = `${SERVER_API}${TRANSCRIBE_API}/`;
export const GET_TRANSCRIBE_DETAIL_API = `${SERVER_API}${TRANSCRIBE_API}/detail/`;
export const GET_TRANSCRIBE_AUDIO_API = `${SERVER_API}${TRANSCRIBE_API}/audio/`;
export const UPLOAD_TRANSCRIBE_FILE_API = `${SERVER_API}${TRANSCRIBE_API}/upload/file`;
export const UPLOAD_TRANSCRIBE_YOUTUBE_API = `${SERVER_API}${TRANSCRIBE_API}/upload/youtube/`;
export const DELETE_TRANSCRIBE_API = `${SERVER_API}${TRANSCRIBE_API}/delete/`;

// SYNTHESIS
export const GET_SYNTHESIS_LIST_API = `${SERVER_API}${SYNTHESIS_API}/`;
export const GET_SYNTHESIS_DETAIL_API = `${SERVER_API}${SYNTHESIS_API}/detail/`;
export const GET_SYNTHESIS_AUDIO_API = `${SERVER_API}${SYNTHESIS_API}/audio/`;
export const UPLOAD_SYNTHESIS_FILE_API = `${SERVER_API}${SYNTHESIS_API}/upload/file/`;
export const UPLOAD_SYNTHESIS_TEXT_API = `${SERVER_API}${SYNTHESIS_API}/upload/text/`;
export const DELETE_SYNTHESIS_API = `${SERVER_API}${SYNTHESIS_API}/delete/`;


// MONITORING


// CHAT
