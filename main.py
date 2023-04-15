from audio_tools import *
import matplotlib.pyplot as plt
import numpy as np


## These two functions were used to record wav files of steps.
#calibrate_mouse()
#record_samples(GEN_FILENAME)


GEN_FILENAME = 'samples/output'


def fourier(aa, pl=True):
    sp = np.fft.fft(aa)
    freq = np.fft.fftfreq(aa.shape[-1])
    if pl:
        plt.plot(freq, sp.real, freq, sp.imag, alpha=.5)
        plt.show()
    return sp



FILENAME = GEN_FILENAME+"1.wav"

play_wav(FILENAME)
plot(FILENAME)


np_sound_ch1 = wav_to_np(outfile = FILENAME)[0]
np_sound_ch2 = wav_to_np(outfile = FILENAME)[1]

fourier(np_sound_ch1)

# Trying to find correlations between

def ltwonorm(aa):
    return np.sqrt(np.sum(aa**2))

vec1, vec2, vec3  = [], [], []
deg = []


for j in range(200):
    # comparing
    audio_signals = wav_to_np(GEN_FILENAME + str(j+1) + ".wav")
    a = np.copy(audio_signals[0]).reshape(-1)[3350:5000]
    b = np.copy(audio_signals[1]).reshape(-1)[3350:5000]

    vec1.append(np.mean(np.abs(a))/np.mean(np.abs(b)))
    vec2.append(np.mean(a[b!=0]/b[b!=0]))
    vec3.append(ltwonorm(a)/ltwonorm(b))

    #degrees
    with open('samples/output.txt') as f:
        lines = f.readlines()
        deg.append(float(lines[j-1].split(':')[-1]))


deg = np.array(deg)* np.pi / 180

print('correlatioins: ')
print(np.corrcoef([deg, np.sin(deg), np.tan(deg/2), vec1, vec2, vec3]))

#(np.array(vec1)-1)*(1/4.8)**0.8?


