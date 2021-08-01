import numpy as np
import sliders_namespace as sn

# Global data variable to hold the most recent epoch
curr_data = []

# Creates a sine wave with added noise. Adapted from Python III workshop
# params:
#   times:  array of x-values for creating wave
#   freq:   frquency of wave
#   amp:    amplitude of wave
#   noise:  amount of noise introduced; higher means more noise
# returns: array of y-values corresponding to the specified sine wave
def generateNoisyWave(times, freq, amp, noise):
    
    # This simplifies code later, this basically just creates our noise for us
    if(not isinstance(times, float)):
        noiseArray = noise * np.random.randn(len(times))
    else:
        noiseArray = noise * np.random.randn(1)
    
    sineWave = amp * np.sin(freq * 2 * np.pi * times)
    return sineWave + noiseArray

# Creates a synthetic brain wave for testing purposes. Adapted from Python IV workshop
# params:
#   args.epochDuration: length of epoch in seconds
#   args.samplingRate:  number of samples per second
#   args.tFreq:     frequency of theta wave
#   args.tAmp:      amplitude of theta wave
#   args.tNoise:    amount of noise in theta wave
#   args.bFreq:     frequency of beta wave
#   args.bAmp:      amplitude of beta wave
#   args.bNoise:    amount of noise in beta wave
# returns: a list of [time, voltage] values corresponding to a synthetic brain wave
def generate_data(args = {}):

    global curr_data

    times = np.linspace(0,args.epochDuration,args.samplingRate) # One second at 250Hz
    theta = generateNoisyWave(times, args.tFreq, args.tAmp, args.tNoise) # (time, Freq, Amp, Noise)
    beta = generateNoisyWave(times, args.bFreq, args.bAmp, args.bNoise)

    xy_list = []

    for x in range(0, len(times)):
        xy_list.append([times[x], theta[x] + beta[x]])

    curr_data = xy_list

    # return beta + theta
    return xy_list

# Performs an FFT on an epoch of EEG data.
# params:
#   data:   list of [time, voltage] pairs corresponding to brain wave
#   samp_rate:      samples per second
#   epoch_length:   length of epoch in seconds
# returns list of [frequency, amplitude] pairs corresponding to fourier spectrum
def ffs(data, samp_rate, epoch_length):

    volts = [x[1] for x in data]

    n = len(volts)
    Y = np.fft.fft(volts)/n # fft computing and normalization
    Y = Y[:100 * epoch_length]
    k = np.arange(n)
    T = n*(epoch_length/samp_rate)
    frq = k/T # two sides frequency range
    frq = frq[:100 * epoch_length] # one side frequency range
    amp = np.abs(Y)

    xy_list = []
    for x in range(0, len(frq)):
        xy_list.append([frq[x], amp[x]])

    return xy_list

# ffs function for returning result to Javascript
# params:
#   args.epochDuration: length of epoch in seconds
#   args.samplingRate:  number of samples per second
# returns list of [frequency, amplitude] pairs corresponding to fourier spectrum
def ffs(args = {}):

    global curr_data
    return ffs(curr_data, args.samplingRate, args.epochDuration)

# Creates a power spectrum from an epoch of EEG data.
# params:
#   data:   list of [time, voltage] pairs corresponding to brain wave
#   samp_rate:      samples per second
#   epoch_length:   length of epoch in seconds
# returns list of [frequency, power] pairs corresponding to fourier spectrum
def power_spec(data, samp_rate, epoch_length):
    ffsData = ffs(data, samp_rate, epoch_length)
    for x in ffsData:
        x[1] = x[1]**2

    return ffsData

# Power spectrum function for returning result to Javascript
# params:
#   args.epochDuration: length of epoch in seconds
#   args.samplingRate:  number of samples per second
# returns list of [frequency, amplitude] pairs corresponding to fourier spectrum
def power_spec(args = {}):

    global curr_data
    return power_spec(curr_data, args.samplingRate, args.epochDuration)

# Calculates the theta-beta ratio (TBR) for the most recently stored epoch and returns to Javascript
# Calculation is mean theta power divided by mean beta power
# params:
#   args.epochDuration: length of epoch in seconds
#   args.samplingRate:  number of samples per second
# returns the TBR
def get_TBR_power(args = {}):

    global curr_data

    ffsData = power_spec(curr_data, args.samplingRate, args.epochDuration)

    theta_sum = 0
    theta_count = 0
    beta_sum = 0
    beta_count = 0

    for x in ffsData:
        if x[0] <=7 and x[0] > 3.5:
            theta_sum += x[1]
            theta_count += 1
        elif x[0] <= 20 and x[0] > 12:
            beta_sum += x[1]
            beta_count += 1
    
    return ( (theta_sum / theta_count) / (beta_sum / beta_count) )

    

    