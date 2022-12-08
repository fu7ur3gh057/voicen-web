import React, {useContext, useEffect, useRef, useState} from 'react';
import {PlayerContext} from "../../../context/player/PlayerContext";
import WaveSurfer from "wavesurfer.js";
import {calculateTime, initWaveSurfer} from "../../../utils/playerUtils";
import {useAuthAxios} from "../../../hooks/useAuthAxios";
import {GET_TRANSCRIBE_AUDIO_API} from "../../../constants/apiConstants";

const WavePlayer = () => {
    const waveColor = '#8b8888';
    const progressColor = '#2E84FF';
    const authAxios = useAuthAxios();
    // Context
    const playerContext = useContext(PlayerContext);
    const {state, dispatch} = playerContext!;

    // States
    const [isPlaying, setIsPlaying] = useState(false);
    const [isRepeating, setIsRepeating] = useState(false);
    const [progressTime, setProgressTime] = useState('');
    const [durationTime, setDurationTime] = useState('');

    // Refs
    // const audioRef = useRef<string>();
    // const trackRef = useRef<HTMLAudioElement | any>();
    const waveContainerRef = useRef<HTMLElement | any>();
    const waveRef = useRef<WaveSurfer>();
    const repeatModeRef = useRef<boolean>(false);

    // Effects
    // New Audio Effect, all wavesurfer events
    useEffect(() => {
        if (state.fileUrl === '') return;
        waveRef.current = initWaveSurfer(waveContainerRef.current, waveColor, progressColor);
        // waveRef.current?.load(trackRef.current);

        uploadAudioData();

        // onReady
        waveRef.current?.on('ready', () => {
            setDurationTime(calculateTime(waveRef.current?.getDuration()!));
            console.log(`duration - ${waveRef.current?.getDuration()!}`);
            waveRef.current?.play();
        })

        // onPlay
        waveRef.current?.on('play', () => {
            setIsPlaying(true);
        })

        // onPause
        waveRef.current?.on('pause', () => {
            setIsPlaying(false);
        })
        // onProcess
        waveRef.current?.on('audioprocess', () => {
            if (waveRef.current?.isPlaying()) {
                setIsPlaying(true);
                setProgressTime(calculateTime(waveRef.current?.getCurrentTime()));
            } else setIsPlaying(false);
        })
        // onSeek
        waveRef.current?.on('seek', () => {
            console.log(`curr time ${waveRef.current?.getCurrentTime()!}`)
            setProgressTime(calculateTime(waveRef.current?.getCurrentTime()!));
        })
        // onFinish
        waveRef.current?.on('finish', () => {
            if (repeatModeRef.current) {
                waveRef.current?.play(0);
                setIsPlaying(true);
            } else setIsPlaying(false)

        })
        return () => {
            waveRef.current?.stop();
            waveRef.current?.destroy();
        }
    }, [state.fileUrl]);

    const uploadAudioData = async () => {
        const response = await authAxios.get(`${GET_TRANSCRIBE_AUDIO_API}${state.fileUrl}/`, {
            responseType: 'arraybuffer'
        });
        if (!response.status) {
            console.log('something went wrong')
            throw new Error('Cant get Audio File, Server Error');
        } else {
            if (response.request.responseType === 'arraybuffer' && response.data.toString() === '[object ArrayBuffer]') {
                console.log('requestType is arraybuffer')
                const buffer = response.data.arrayBuffer();
                const audioCtx = new AudioContext();
                let decodedData = await audioCtx.decodeAudioData(buffer);
                waveRef.current?.loadDecodedBuffer(decodedData);
            } else {
                console.log('requestType is NOT arraybuffer')
                console.log(`${response.request.responseType}`)
                console.log(`${response.data}`)
            }

        }
    }

    const handlePlayPause = () => {
        waveRef.current?.playPause();
        if (waveRef.current?.isPlaying()) setIsPlaying(true);
        else setIsPlaying(false);
    }

    const seekForward = () => {
        waveRef.current?.skipForward(0.5)
    }

    const seekBackward = () => {
        waveRef.current?.skipBackward(0.5)
    }

    return (
        <div>
            <button>play</button>
            <div>
                <div ref={waveContainerRef}/>
            </div>
        </div>
    );
};

export default WavePlayer;
