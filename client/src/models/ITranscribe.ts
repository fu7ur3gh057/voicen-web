export interface ITranscribe {
    id: string,
    file_name: string,
    youtube_url: string,
    full_text: string,
    duration: string,
    price: string,
    lang: string,
    status: string,
    created_at: string,
}


export interface ITranscript {
    word: string,
    endTime: number,
    startTime: number,
    confidence: number,
}

export interface ITranscriptList {
    status: {},
    fulltext: string,
    words: ITranscript[],
}
