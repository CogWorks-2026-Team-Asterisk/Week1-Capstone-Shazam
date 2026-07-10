import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from microphone import record_audio
from typing import Tuple, List
from numba import njit
from IPython.display import Audio

# The variables That will be defined later in the full code:
# samples: 1d numpy array
# sample_rate: int




@njit
def _peaks(
    data_2d: np.ndarray,
    nbrhd_row_offsets: np.ndarray,
    nbrhd_col_offsets: np.ndarray,
    amp_min: float
) -> List[Tuple[int, int]]:

    peak_locations = []

    for c, r in np.ndindex(*data_2d.shape[::-1]):

        if data_2d[r, c] <= amp_min:
            continue

        for dr, dc in zip(
            nbrhd_row_offsets,
            nbrhd_col_offsets
        ):
            if dr == 0 and dc == 0:
                continue

            neighbor_row = r + dr
            neighbor_col = c + dc

            if not (0 <= neighbor_row < data_2d.shape[0]):
                continue

            if not (0 <= neighbor_col < data_2d.shape[1]):
                continue

            if data_2d[r, c] < data_2d[neighbor_row, neighbor_col]:
                break

        else:
            peak_locations.append((r, c))

    return peak_locations


def local_peak_locations(data_2d: np.ndarray, neighborhood: np.ndarray, amp_min: float) -> List[Tuple[int, int]]:

    assert neighborhood.ndim == 2
    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1

    # np.where returns row indices and column indices together
    nbrhd_row_indices, nbrhd_col_indices = np.where(neighborhood)

    nbrhd_row_offsets = (
        nbrhd_row_indices - neighborhood.shape[0] // 2
    )

    nbrhd_col_offsets = (
        nbrhd_col_indices - neighborhood.shape[1] // 2
    )

    return _peaks(
        data_2d,
        nbrhd_row_offsets,
        nbrhd_col_offsets,
        amp_min
    )


def identifying_peaks(
    samples: np.ndarray,
    sample_rate: int,
    fft_pts: int = 4096,
    noverlap: int = 2048,
    neighborhood_size: int = 15,
    amplitude_percentile: float = 99
) -> Tuple[
    List[Tuple[int, int]],
    np.ndarray,
    np.ndarray,
    np.ndarray
]:

    spectrogram, frequencies, times = mlab.specgram(
        samples,
        NFFT=fft_pts,
        Fs=sample_rate,
        noverlap=noverlap
    )

    log_spectrogram = np.log10(spectrogram + 1e-20)

    if neighborhood_size % 2 == 0:
        raise ValueError("neighborhood_size must be odd")

    neighborhood = np.ones(
        (neighborhood_size, neighborhood_size),
        dtype=np.bool_
    )

    amp_min = np.percentile(
        log_spectrogram,
        amplitude_percentile
    )

    peak_locations = local_peak_locations(
        log_spectrogram,
        neighborhood,
        amp_min
    )

    return peak_locations, frequencies, times, log_spectrogram
    
    
# Debug/testing
    
# test_spectrogram = np.array([
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 2, 1, 0, 1, 8, 0],
#     [0, 1, 9, 1, 0, 1, 0],
#     [0, 0, 1, 0, 0, 0, 0],
#     [0, 6, 0, 0, 7, 1, 0],
#     [0, 0, 0, 0, 1, 0, 0]
# ], dtype=np.float64)

# neighborhood = np.ones((3, 3), dtype=np.bool_)
# amp_min = 5.0

# detected_peaks = local_peak_locations(
#     test_spectrogram,
#     neighborhood,
#     amp_min
# )

# print(detected_peaks)


# Creating fingerprints (doing it later)

def create_fingerprints(peaks: List[Tuple[int, int]], fanout: int = 5, min_time_delta: int = 1, max_time_delta: int = 50) -> List[Tuple[Tuple[int, int, int], int]]:
    