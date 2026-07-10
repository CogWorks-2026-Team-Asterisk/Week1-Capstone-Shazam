import os
from pathlib import Path

import librosa
import numpy as np


def load_song(file_path):
    # load the song as mono audio at 44100 Hz
    samples, rate = librosa.load(file_path, sr=44100, mono=True)

    # librosa gives floats from -1 to 1, turn them into int16 like the mic recordings
    samples = (samples * 32767).astype(np.int16)
    return samples, rate


def convert_all_songs(song_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for song in Path(song_folder).iterdir():
        samples, rate = load_song(song)

        # save as [sample_rate, samples...] just like record_and_save does
        np.save(Path(output_folder) / (song.stem + ".npy"), np.hstack((rate, samples)))
        print("converted", song.name)


convert_all_songs("song_list", "song_samples")