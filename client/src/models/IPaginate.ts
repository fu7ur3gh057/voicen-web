export interface IPaginate<T> {
    count: number,
    next?: string,
    previous?: string,
    results: T[],
}
