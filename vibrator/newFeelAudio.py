import numpy as np
from scipy.signal import butter, lfilter
import matplotlib
import os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import sounddevice as sd
import math
fs = 44100
sd.default.samplerate = 44100

def arbitraryWave(duration, function):
    """Returns list of length duration*sampling frequency where each point is defined by function(i) where i is the ith position
    :param duration: int of duration in seconds
    :param function: function that takes int in and returns a float -1 to 1
    Raises ValueError if function returns something out of the range -1 to 1
    """
    audio = []
    for i in range(0, duration*sd.default.samplerate):
        value = function(i)
        if value <= 1 and value >= -1:
            audio.append(function(i))
        else:
            raise ValueError("Function returned '{0}' which is not between -1 and 1".format(value))
    return audio

def sineWave(freq, duration):
    """Returns list of a sinewave -1 to 1
    :param freq: frequency of sine wave in hertz
    :param duration: duration of sine wave in seconds
    """
    omega = (math.pi*2)*(freq/sd.default.samplerate)
    return arbitraryWave(duration, lambda i: np.sin(omega*i))

def squareWave(freq, duration, dutyCycle):
    """Returns list of a square wave 0 to 1
    :param freq: frequency in hertz
    :param duration: duration of sample generated in seconds 
    :param dutyCycle: 0-1 for 0-100% duty cycle
    """
    period = int(sd.default.samplerate/freq)
    return arbitraryWave(duration, lambda i: int((i%period)<=(dutyCycle*period)))

def scaleVolume(audio, scalar):
    """Returns list with scaled entries. Eg. list in: [a, b, c, ...] output would be [scalar*a, scalar*b, scalar*c, ...]
    :param audio: input list
    :param scalar: scalar value
    """
    for i in range(0, len(audio)):
        audio[i]=audio[i]*scalar
    return audio

def combineAudio(audioList, multiply=False, add=False):
    """Returns an list where each element is the product/sum of each element of the lists in audioList
       eg. if the input is [[a,b,c],[d,e,f]] and multiply is set to True the output would be [a*d, b*e, f*c]
    :param audioList: List of audio samples, must be same length
    :param multiply: Set to True to multiply data points
    :param add: Set to True to add data points
    Raises IndexError when lists are not the same length
    Raises ValueError if multiply and add are the same values
    """
    if multiply==add:
        raise ValueError("multiply and add cannot be the same value")
    if multiply:
        newAudio = [1]*len(audioList[0])
    if add:
        newAudio = [0]*len(audioList[0])
    for i in range(len(audioList[0])):
        for j in range(len(audioList)):
            if multiply:
                newAudio[i] = audioList[j][i]*newAudio[i]
            if add:
                newAudio[i] = audioList[j][i]+newAudio[i]
    return newAudio

def importWav(filename):
    """Imports wave file and returns list
    :param filename: file name
    """
    a = read(filename)
    b = np.array(a[1],dtype=float)
    audio = []
    depth = 2**16
    for x in b:
        audio.append(float(x/depth))
    return audio

def delayAudio(audio, delay, extend=False):
    """Delays audio by inserting silence (0s) at the beginning of the sound clip
    :param audio: list that contains audio sample
    :param delay: time in seconds to delay the sound
    :param extend: if True, will add padding to beginning and shift sound resulting in a longer list
                   if False, will add padding to beginning and clip sound to keep list the same length
                   default: False
    """
    sampleDelay = int(delay*sd.default.samplerate)
    audio = ([0]*sampleDelay)+audio #concatenate lists
    if not extend:
        audio = audio[0:len(audio)-sampleDelay]
    return audio 

def setVolume(audio, magnitude):
    """Takes in audio and scales it such that the largest value has a specific magnitude
    :param audio: list that contains audio sample
    :param magnitude: what to scale the largest value's magnitude to (float 0-1)
    """
    #find max value
    minValue = min(audio)
    maxValue = max(audio)
    maxMagValue = minValue if abs(minValue)>maxValue else maxValue
    
    scalar = magnitude/maxMagValue
    
    return list(map(lambda x: x*scalar, audio))

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

dur = 1 
scl = 1 
sixty = sineWave(60/scl, int(dur*scl))
one = squareWave(1/scl, int(dur*scl), 0.5)
oneTwo = sineWave(1/scl, int(dur*scl))
newfinal = combineAudio([sixty, one, oneTwo], multiply=True)
newfinal = setVolume(newfinal, 0.25)
sd.play(scaleVolume(newfinal, 1), blocking=True, loop=True)
