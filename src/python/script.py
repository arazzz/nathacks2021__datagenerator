import numpy as np
import sliders_namespace as sn

#to import (for each frequency)
#   length of epoch
#   # of samples
#   freq
#   amp
#   noise

# returns
curr_data = []

def generateNoisyWave(times, freq, amp, noise):
    
    # This simplifies code later, this basically just creates our noise for us
    if(not isinstance(times, float)):
        noiseArray = noise * np.random.randn(len(times))
    else:
        noiseArray = noise * np.random.randn(1)
    
    
    sineWave = amp * np.sin(freq * 2 * np.pi * times)
    return sineWave + noiseArray

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

def power_spec(data, samp_rate, epoch_length):
    ffsData = ffs(data, samp_rate, epoch_length)
    for x in ffsData:
        x[1] = x[1]**2

    return ffsData

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

    

    