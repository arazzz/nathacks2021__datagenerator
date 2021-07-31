import numpy as np
import matplotlib.pyplot as plt
#import sliders_namespace as sn

#to import (for each frequency)
#   length of epoch
#   # of samples
#   freq
#   amp
#   noise

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

    times = np.linspace(0,3,512) # One second at 250Hz
    theta = generateNoisyWave(times, 5, 10, 2) # (time, Freq, Amp, Noise)
    beta = generateNoisyWave(times, 15, 5, 2)

    xy_list = []

    for x in range(0, len(times)):
        xy_list.append([times[x], theta[x] + beta[x]])

    return beta + theta

    # plt.plot(times, y)
    # plt.show()

def fft(series):
    fftData = np.fft.fft(series)/len(series)
    freq = np.fft.fftfreq(len(series))*512

    freq = freq[0:50]
    fftData = fftData[0:50]

    plt.plot(freq, fftData.imag)
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

def freqSpec(data):
    n = len(data)
    Y = np.fft.fft(data)/n # fft computing and normalization
    Y = Y[:100 * 3]
    k = np.arange(n)
    T = n*(3/512)
    frq = k/T # two sides frequency range
    frq = frq[:100 * 3] # one side frequency range
    amp = np.abs(Y)
    xy_list = []
    for x in range(0, len(frq)):
        xy_list.append([frq[x], amp[x]])

    return xy_list

def power_spec(data):
    ffsData = freqSpec(data)
    for x in ffsData:
        x[1] = x[1]**2

    return ffsData

def plotFS(data):

    ps = power_spec(data)

    frq = [x[0] for x in ps]
    pw = [x[1] for x in ps]

    plt.plot(frq, pw)
    plt.show()

#fft(generate_data())
plotFS(generate_data())
