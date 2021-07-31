import numpy as np
import sliders_namespace as sn

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

def generate_data(args = {}):

    times = np.linspace(0,args.epochDuration,args.samplingRate) # One second at 250Hz
    theta = generateNoisyWave(times, args.tFreq, args.tAmp, args.tNoise) # (time, Freq, Amp, Noise)
    beta = generateNoisyWave(times, args.bFreq, args.bAmp, args.bNoise)

    xy_list = []

    for x in range(0, len(times)):
        xy_list.append([times[x], theta[x] + beta[x]])

    # return beta + theta
    return xy_list