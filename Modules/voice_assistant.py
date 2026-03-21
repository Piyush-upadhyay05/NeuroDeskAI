import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np
from Modules.ai_brain import ask_ai
from Modules import Automation

current_app = None

engine = pyttsx3.init()

# ------------------------
# Speak Function
# ------------------------
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ------------------------
# Listen Function (sounddevice version)
# ------------------------
def listen():
    samplerate = 16000
    duration = 5

    print("Listening...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    sf.write("temp.wav", recording, samplerate)

    r = sr.Recognizer()

    try:
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)

        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()

    except:
        speak("Sorry I did not understand")
        return ""


# ------------------------
# Command Handler
# ------------------------
def process_command(command):

    global current_app

    if "open chrome" in command:
        speak("Opening Chrome sir")
        Automation.open_chrome()
        current_app = "chrome"

    elif "open notepad" in command:
        speak("Opening Notepad sir")
        Automation.open_notepad()
        current_app = "notepad"

    elif "open calculator" in command:
        speak("Opening Calculator sir")
        Automation.open_calculator()
        current_app = "calculator"

    elif "go to desktop" in command:
        speak("Showing desktop sir")
        Automation.show_desktop()

    elif "switch window" in command:
        speak("Switching window sir")
        Automation.switch_window()

    elif "close window" in command:
        speak("Closing the window sir")
        Automation.close_window()

    elif "take screenshot" in command:
        speak("Taking screenshot sir")
        file = Automation.take_screenshot()
        speak("Screenshot saved sir")

    elif "open documents" in command:
        speak("Opening documents folder sir")
        Automation.open_folder("documents")
        current_app = "document"

    elif "open downloads" in command:
        speak("Opening downloads folder sir")
        Automation.open_folder("downloads")

    elif "open project folder" in command:
        found = Automation.search_folder("project")

        if found:
            speak("Opening folder sir")
        else:
            speak("Folder not found sir")

    elif "exit" in command:
        speak("Goodbye Piyush sir")
        return False
    
    elif current_app == "notepad":
        
        if "write" in command:
            text = command.replace("")
            speak("Writing in notepad sir")
            Automation.type_text(text)

        elif "new line" in command:
            Automation.press_enter()

        elif "save file" in command:
            speak("Saving file sir")
            Automation.hotkey("ctrl", "s")
    
    elif current_app == "chrome":

        if "search" in command:
            query = command.replace("search", "")
            speak("Searching on Google sir")
            Automation.type_text(query)
            Automation.press_enter()

        elif "scroll down" in command:
            Automation.scroll_down()

        elif "scroll up" in command:
            Automation.scroll_up()
    else:
        speak("Let me think sir")
        answer = ask_ai(command)
        speak(answer)

    return True


# ------------------------
# Main Loop
# ------------------------
def run_assistant():

    speak("Hello Piyush sir, NeuroDesk AI is ready for your command.")

    running = True

    while running:
        command = listen()

        if command:
            running = process_command(command)


if __name__ == "__main__":
    run_assistant()
