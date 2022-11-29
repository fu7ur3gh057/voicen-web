export interface IAccessTokenInfo {
    token_type: string,
    exp: number,
    jti: string,
    user_id: string,
    name: string,
    email: string,
}

export interface ITokens {
    refresh: string,
    access: string
}

export interface IUser {
    id: string,
    username: string,
    email: string,
    first_name: string,
    last_name: string,
    full_name: string,
    is_verified?: string,
    is_active?: string,
}
