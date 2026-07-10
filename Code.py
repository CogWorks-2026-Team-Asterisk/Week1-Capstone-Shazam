import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from microphone import record_audio
from typing import Tuple, List
from numba import njit
from IPython.display import Audio
from microphone import record_audio
#%matplotlib notebook


SAMPLING_RATE = 44100 # Hz


def record_and_save(listen_time: float, file_path: str):
    frames, sample_rate = record_audio(listen_time)

    samples = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    array_to_save = np.hstack((sample_rate, samples))

    np.save(file_path, array_to_save)

def load_and_parse(file_path: str) -> Tuple[np.ndarray, int]:
    loaded_array = np.load(file_path)
    
    sample_rate = loaded_array[0]
    signal = loaded_array[1:]
    
    return signal, sample_rate


record_and_save(listen_time=5, file_path="song_samp.npy")
samples, sample_rate = load_and_parse(file_path="song_samp.npy")  #load the song_samp.npy recording





'''
@njit
def _peaks(
    data_2d: np.ndarray, nbrhd_row_offsets: np.ndarray, nbrhd_col_offsets: np.ndarray, amp_min: float) -> List[Tuple[int, int]]:
    peaks = []  # stores the (row, col) locations of all the local peaks

    for c, r in np.ndindex(*data_2d.shape[::-1]):
        if data_2d[r, c] <= amp_min:
            continue
        
        for dr, dc in zip(nbrhd_row_offsets, nbrhd_col_offsets):
            if dr == 0 and dc == 0:
                # This would compare (r, c) with itself.. skip!
                continue

            if not (0 <= r + dr < data_2d.shape[0]):
                # neighbor falls outside of boundary.. skip!
                continue

            if not (0 <= c + dc < data_2d.shape[1]):
                # neighbor falls outside of boundary.. skip!
                continue

            if data_2d[r, c] < data_2d[r + dr, c + dc]:
                # One of the amplitudes within the neighborhood
                # is larger, thus data_2d[r, c] cannot be a peak
                break
        else:
            # if we did not break from the for-loop then (r, c) is a local peak
            peaks.append((r, c))
    return peaks

def local_peak_locations(data_2d: np.ndarray, neighborhood: np.ndarray, amp_min: float):

    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1

    nbrhd_row_offsets = nbrhd_row_indices - neighborhood.shape[0] // 2
    nbrhd_col_offsets = nbrhd_col_indices - neighborhood.shape[1] // 2

    return _peaks(data_2d, nbrhd_row_offsets, nbrhd_col_offsets, amp_min=amp_min)








'''