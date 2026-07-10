import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from typing import Tuple

from microphone import record_audio

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


record_and_save(listen_time=5, file_path="digital_signal.npy")
samples, sample_rate = load_and_parse(file_path="digital_signal.npy")  #load the digital_signal.npy recording

Audio(samples, rate=sample_rate)