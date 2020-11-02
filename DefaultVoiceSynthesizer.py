import pyttsx3 as tts
from pyttsx3 import *

voice = tts.init("sapi5", True)
def generateresponse(question):
    response = ""

    return response

def say(texttospeak):
    voice.say(texttospeak)
    voice.runAndWait()

'''import scipy.io.wavfile as wav
import numpy
WAV16BITMAX = 65536
samplerate, samples = wav.read("Warframe Ordis Quotes 2.wav")
lowerhalf, upperhalf =[], []
for sample in samples:
    if sample >0:
        upperhalf.append(sample)
    elif sample < 0:
        lowerhalf.append(sample)
print(max(upperhalf), min(lowerhalf))
numpy.fft.rfft()
'''