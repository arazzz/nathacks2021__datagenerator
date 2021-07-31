import numpy as np
import matplotlib.pyplot as plt

#to import (for each frequency)
#   length of epoch
#   # of samples
#   freq
#   amp
#   noise

srate = 250
# returns
epoch = []
spectrum = []
bins = []

def generateNoisyWave(times, freq, amp, noise):
    
    # This simplifies code later, this basically just creates our noise for us
    if(not isinstance(times, float)):
        noiseArray = noise * np.random.randn(len(times))
    else:
        noiseArray = noise * np.random.randn(1)
    
    
    sineWave = amp * np.sin(freq * 2 * np.pi * times)
    return sineWave + noiseArray

def generate_data():

    times = np.linspace(0,1,srate) # One second at 250Hz
    theta = generateNoisyWave(times, 6, 10, 1) # (time, Freq, Amp, Noise)
    beta = generateNoisyWave(times, 16, 5, 1)

    return theta + beta

    # plt.plot(times, y)
    # plt.show()

def fft(series):
    fftData = np.fft.rfft(series)
    freq = np.fft.fftfreq(len(series))*srate

    freq = freq[0:50]
    fftData = fftData[0:50]

    plt.plot(freq, fftData)
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

fft(generate_data())
