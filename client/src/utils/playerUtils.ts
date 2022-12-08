import WaveSurfer from "wavesurfer.js";

export const initWaveSurfer = (container: string | HTMLElement, color: string, progressColor: string) => {
    return WaveSurfer.create({
        barWidth: 3,
        cursorWidth: 0,
        barMinHeight: 1,
        barRadius: 3,
        container: container,
        backend: 'WebAudio',
        height: 40,
        progressColor: `${progressColor}`,
        responsive: true,
        waveColor: `${color}`,
        // cursorColor: '#5215b7',
    });
}

export const calculateTime = (time: number) => {
    const hours = Math.floor(time / 3600)
    const returnedHours = `${hours}`

    const minutes = Math.floor(time / 60);
    const returnedMinutes = minutes < 10 ? `0${minutes}` : `${minutes}`

    const seconds = (time - minutes * 60);
    const returnedSeconds = seconds < 10 ? `0${Math.trunc(seconds)}` : `${Math.trunc(seconds)}`

    const result = `${returnedHours}:${returnedMinutes}:${returnedSeconds}`;
    return result;
};


function padTo2Digits(num: number) {
    return num.toString().padStart(2, '0');
}

export function convertMsToHM(milliseconds: number) {
    let seconds = Math.floor(milliseconds / 1000);
    let minutes = Math.floor(seconds / 60);

    let hours = Math.floor(minutes / 60);

    seconds = seconds % 60;
    // 👇️ if seconds are greater than 30, round minutes up (optional)
    minutes = seconds >= 30 ? minutes + 1 : minutes;

    minutes = minutes % 60;

    const mSec = milliseconds / 1000
    const floatNumber = 3
    const fractionalMsec = Math.floor((mSec % 1) * Math.pow(10, floatNumber));

    // 👇️ If you don't want to roll hours over, e.g. 24 to 00
    // 👇️ comment (or remove) the line below
    // commenting next line gets you `24:00:00` instead of `00:00:00`
    // or `36:15:31` instead of `12:15:31`, etc.
    hours = hours % 24;
    return `${hours}:${padTo2Digits(minutes)}:${padTo2Digits(seconds)},${padTo2Digits(fractionalMsec)}`;
}


export const splitFileName = (fileName: string) => {
    return fileName.split(/_(.*)/s)[1]
}

export const getProgressPercent = (currTime: number, totalDuration: number) => {
    const result = (currTime / totalDuration) / 1000
    return Number(result.toFixed(5))
}
