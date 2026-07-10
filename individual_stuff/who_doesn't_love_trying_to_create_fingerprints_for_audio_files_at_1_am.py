from pathlib import Path
import numpy as np
import librosa

def load_song(file_path: str):
    # load the song as mono audio at 44100 Hz
    samples, rate = librosa.load(file_path, sr=44100, mono=True)

    # librosa gives floats from -1 to 1, turn them into int16 like the mic recordings
    samples = (samples * 32767).astype(np.int16)
    return samples, rate

fft_output = np.fft.fft()
magnitudes = np.abs(fft_output)