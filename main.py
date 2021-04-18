from vosk import Model, KaldiRecognizer
import os
import time
import pyaudio
import random
import Xlib
from Xlib import display, X   # X is also needed

display = Xlib.display.Display()
screen = display.screen()
root = screen.root

#draw_it(root.get_attributes())
root.change_attributes(event_mask=X.ExposureMask)  # "adds" this event mask
#draw_it(root.get_attributes())  # see the difference

gc = root.create_gc(foreground = screen.white_pixel, background = screen.black_pixel)

def draw_it(output):
    root.draw_text(gc, 100, 100, output.encode())
    display.flush()

def run(command):
    os.system(command)
    os.system("aplay bleep.wav")

def speak(text):
    if text == "Welcome Sequence":
        os.system("mpg123 -q lines/prehub06.mp3")
    else:
        os.system("echo " + text + " | festival --tts")
        #os.system("mpg123 -q say.mp3")

def greeting():
    path="/home/wilson/lib/portal/Cave Johnson/PTI/"
    files=os.listdir(path)
    d=random.choice(files)
    os.system("mpg123 -q /home/wilson/lib/portal/Cave\ Johnson/PTI/" + d)
    draw_it("--------------------------------------------------------------------")

def takeCommand():
    data = stream.read(700)
    if len(data) == 0:
        return ""
    if rec.AcceptWaveform(data):
        stage1 = rec.Result()
        stage2 = stage1.split('"text" : "')[1]
        result = stage2.split('"\n}')[0]
        if result != "":
            draw_it(result)
        return result
    else:
        return ""

if __name__=='__main__':
    draw_it("Init")
    speak("Welcome Sequence")
    if not os.path.exists("model"):
        draw_it ("Model needed, but not found.")
        exit (1)

    global rec
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    global stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    greeting()
    while True:
        statement = takeCommand()
        if statement=="":
            continue
        else:
            if "open" in statement or "load" in statement:
                if "term" in statement:
                    run("st &")
                if "browser" in statement or " brave" in statement:
                    run("brave &")
                if "atom" in statement or "editor" in statement:
                    run("atom &")
            elif " lock " in statement:
                run("slock &")
            elif "drop my needle" in statement:
                run("cd ~/lib/music && mpv * &")
            if ("create" in statement or "make" in statement or "start" in statement) and "project" in statement:
                name = ""
                while name == "":
                    name = takeCommand()
                run("cd ~/lib/code && mkdir " + name)
            elif "bye" in statement:
                speak("Goodbye")
                draw_it("--------------------------------------------------------------------")
                break
