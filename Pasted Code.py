import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks

""" 'short time fourier transform' (STFT) of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(int(np.floor(frameSize/2.0))), sig)
    # cols for windowing
    cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(int(cols), frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

""" scale frequency axis logarithmically """
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)
    # timebins = How many units of time measured
    # freqbins = How many samples were taken in each unit of time

    scale = np.linspace(0, 1, freqbins) ** factor #This creates a scaling factor of some kind?
    scale *= (freqbins-1)/max(scale) #the sample rate over the highest decibel? what?
    scale = np.unique(np.round(scale)) #rounds everything in the list of amplitudes, and removes any duplicates

    # create spectrogram with new freq bins
    #frequency bins are intervals between samples in frequency domain.
    newspec = np.complex128(np.zeros([timebins, len(scale)])) #creates a new array of complex numbers...
    #...with <seconds recorded> dimensions, and <samples per sec> items in each dimension...
    #...but what is the complex part for exactly?

    #We're basically breaking the data down and creating intervals of sound.
    for i in range(0, len(scale)): #for everything in the list of amplitudes
        if i == len(scale)-1: #some special condition for the last item in the list
            newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis=1) #sets the sample at...
            #...newspec[i] in every list to be the sum of each individual set of samples...
            # ...in the second from scale[i] to the end
        else:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)
            #Here it sets the sample at newspec[i] in every list to be: spec[scale[i]]+spec[scale[i+1]]

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])

    freqs = [] # the frequency of every sample
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[int(scale[i]):])]
        else:
            freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i+1])])]

    return newspec, freqs

""" plot spectrogram"""
def plotstft(audiopath, binsize=2**10, plotpath=None, colormap="jet"):
    samplerate, samples = wav.read(audiopath)

    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)

    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    print("timebins: ", timebins)
    print("freqbins: ", freqbins)

    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    if plotpath:
        plt.savefig(plotpath, bbox_inches="tight")
    else:
        plt.show()

    plt.clf()

    return ims
if False:
    filepath = "../Assets/Kim Jong Un - Baka Mitai (Deepfake).wav"
else:
    filepath = "../Assets/Warframe Ordis Quotes 2.wav"
ims = plotstft(filepath)
'''import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

sample_rate, samples = wavfile.read('Kim Jong Un - Baka Mitai (Deepfake).wav')
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
print(spectrogram)
plt.pcolormesh(times, frequencies, spectrogram)
plt.imshow(spectrogram)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()'''