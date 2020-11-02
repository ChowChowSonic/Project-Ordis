import librosa
import torch

tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2',map_location=torch.device('cpu'))
print("download complete!")
audio_data = 'Assets/Warframe Ordis Quotes 2.wav'

'''
data , samplingrate = librosa.load(audio_data)
print(type(data), type(samplingrate))#<class 'numpy.ndarray'> <class 'int'>print(x.shape, sr)#(94316,) 22050
spectral_centroids = librosa.feature.spectral_centroid(data, sr=samplingrate)[0]
spectral_rolloff = librosa.feature.spectral_rolloff(data+0.01, sr=samplingrate)[0]
#mfccs = librosa.feature.mfcc(data, sr=fs)'''