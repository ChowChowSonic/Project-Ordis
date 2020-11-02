import pyaudio
import speech_recognition as sr
import wave
import threading
import audioop
import math

#I was hoping to keep OOP logic out of my Python but Screw Keeping Things Consistent™ AM I RIGHT
class audioRecorder(threading.Thread):
    def __init__(self, ThreadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = ThreadID
        self.name = name
        self.counter = counter

    def run(self):
        record()

defaultopenthread = audioRecorder(1, "Audio", 1)
FORMAT = pyaudio.paInt16 # dont know dont care dont mess.
CHANNELS = 1 # Mono vs sterio im guessing?
RATE = 44100 # the bitrate of the audio...?
CHUNK = 1024 # dont know dont care dont mess.
RECORDING = False
WAVE_OUTPUT_FILENAME = "../Assets/file.wav"
recorder = sr.Recognizer()

stream = "" # the input stream
frames = [] # The 'audio frames' that will be written to a file

# start Recording
def record():
    audio = pyaudio.PyAudio()  # according to the documentation this initializes the port audio
    frames = []  # sets the frames equal to nothing so that each recording stays seperate
    num_silent = 0
    snd_started = False
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...", end=' ')
    # opens the audio stream
    while 1:
      data = stream.read(CHUNK)  # Break the data stream into readable chunks
      silent = (20*math.log10(0.1+audioop.rms(data, 2)) < 40)  # Decibel = 20 * log10(rms(data))
      if not silent or snd_started:
          frames.append(data)  # adds the chunk to the list of sound bytes
      # rms(data) = sqrt(sum(data)/length(data))
      if silent and snd_started:
          num_silent += 1
      elif not silent and not snd_started:
          snd_started = True

      if snd_started and (num_silent > 60):
          break

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("finished recording")

# writes everything to a file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def recordandrecognise():
    try:
        defaultopenthread.run()
        file = sr.AudioFile('../Assets/file.wav')
        with file as source:
            audio = recorder.record(source)
        try:
            speech = recorder.recognize_google(audio)
        except:
            speech = recorder.recognize_sphinx(audio, "EN-US")
        speech = speech.replace("+", "plus")
        speech = speech.replace("-", "minus")
        speech = speech.replace("*", "times")
        speech = speech.replace("/", "over")
        return speech
    except sr.UnknownValueError:
       return "Speech unintelligible"
    except sr.RequestError:
       print("Error with installation")
    except Exception as e:
      print(type(e), e.args)