export interface IWallet {
    email: string,
    username: string,
    credit: string,
}

export interface ITransaction {
    id: string,
    amount: string,
    type: number,
    created_at: string,
}

export interface ISubscription {
    pkid: string,
    id: string,
    created_at: string,
    updated_at: string,
    type: string,
    end_time: string,
    wallet: string,
}

export interface IOperation {
    id: string,
    amount: string,
    type: number,
    created_at: string,
}
