import numpy as np
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