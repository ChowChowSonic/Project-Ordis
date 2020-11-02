import AudioRecorder
import SpeechProcessor as sp
import DefaultVoiceSynthesizer as synth

print("Loading speech recognition and key phrases...")
EXITPHRASE = "leave"
# " You cannot declare a variable or value as constant in Python. Just don't change it. "
# Motherfuckers.

while True:
    try:
        speech = AudioRecorder.recordandrecognise()
        print(speech)
        if speech == EXITPHRASE:
            break
        if speech != "Speech unintelligible":
            sp.comprehendspeech(speech)
        else:
            synth.say("I couldnt quite catch that. Please try to speak clearly and concisely")
    except Exception as e:
        print(e)
        synth.say("That raised some kind of error I dunno lmao")
