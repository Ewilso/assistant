from vosk import Model, KaldiRecognizer
import gtts
import datetime
import os
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize
import pyaudio

def speak(text):
    tts = gtts.gTTS(text)
    tts.save("say.mp3")
    os.system("mpg123 -q say.mp3")

def greeting():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good morning. How can I help you?")
    elif hour>=12 and hour<18:
        speak("Good afternoon. How can I help you?")
    else:
        speak("Good evening. How can I help you?")

def takeCommand():
    data = stream.read(4000)
    if len(data) == 0:
        return ""
    if rec.AcceptWaveform(data):
        stage1 = rec.Result()
        stage2 = stage1.split('"text" : "')[1]
        result = stage2.split('"\n}')[0]
        print(result)
        return result
    else:
        return ""

if __name__=='__main__':
    greeting()
    if not os.path.exists("model"):
        print ("Model needed, but not found.")
        exit (1)

    global rec
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    global stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        statement = takeCommand()
        if statement=="":
            continue
        if "goodbye" in statement or "bye" in statement:
            speak('Goodbye for now')
            break
        if "stop " in statement and "music" in statement:
            speak('Of course')
            os.system("mpc clear")
        if "play " in statement and "music" in statement:
            speak('Right away')
            os.system("cd ~/lib/music && mpc add * && mpc toggle &")
