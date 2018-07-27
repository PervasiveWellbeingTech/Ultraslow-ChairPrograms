import numpy as np
import sounddevice as sd
import time

fs = 44100
data = np.random.uniform(-1, 1, fs)
sd.play(data, blocking=True)

