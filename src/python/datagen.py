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

    xy_list = []

    for x in range(0, len(times)):
        xy_list.append([times[x], theta[x] + beta[x]])

    return xy_list

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

def freqSpec(data):
    # fft = (np.abs(np.fft.rfft(data, n=data.size)/data.size))**2
    # frq = np.fft.rfftfreq(fft.size) * 1/dt
    # return (frq, fft)
    n = data.shape[0]
    Y = np.fft.rfft(data, n=n)/n  # fft computing and normalization
    Y = Y[1:int(n/2)]
    k = np.arange(n)
    T = n*(1/srate)
    frq = k/T  # two sides frequency range
    frq = frq[1:int(n/2)]  # one side frequency range
    _frq = np.fft.rfftfreq(data.shape[0], d=(1/srate))
    Y_frq = np.abs(Y)**2
    # return (_frq[0:200], Y_frq[0:200])
    return (_frq, Y_frq)

def plotFS(data):
    _frqs, Y_frq = freqSpec(data)
    plt.plot(_frqs, Y_frq)

fft(generate_data())
