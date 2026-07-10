import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio
from typing import Tuple

from microphone import record_audio

listen_time = 5  #seconds
frames, sample_rate = record_audio(listen_time)  #stores recorded audio in frames and sample_rate
