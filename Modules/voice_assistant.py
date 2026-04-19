# ==========================================
# FILE: Modules/voice_assistant.py
# FINAL FIXED VERSION
# Voice + Mic + Commands + AI Response
# ==========================================

import speech_recognition as sr
import pyttsx3
import threading
import time

from Modules.ai_brain import ask_ai
from Modules import Automation


# ==========================================
# GLOBAL
# ==========================================
current_app = None


# ==========================================
# TEXT TO SPEECH (Windows)
# ==========================================
tts_lock = threading.Lock()

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)   # male voice


def speak(text):
    print("Assistant:", text)

    with tts_lock:
        try:
            engine.stop()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("Voice Error:", e)


# ==========================================
# LISTEN FUNCTION (MIC FIXED)
# ==========================================
def listen():
    recognizer = sr.Recognizer()

    # Better sensitivity
    recognizer.energy_threshold = 250
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6
    recognizer.non_speaking_duration = 0.3

    try:
        with sr.Microphone() as source:

            print("Listening... Speak now")

            # Fast noise adjustment
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.2
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        print("Recognizing...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You said:", command)

        return command.lower().strip()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except Exception as e:
        print("Mic Error:", e)
        return ""

# ==========================================
# COMMAND PROCESSOR
# ==========================================
def process_command(command):
    global current_app

    command = command.lower().strip()

    # -------------------------------
    # OPEN CHROME
    # -------------------------------
    if "chrome" in command:
        speak("Opening Chrome sir")
        Automation.open_chrome()
        current_app = "chrome"

    # -------------------------------
    # OPEN NOTEPAD
    # -------------------------------
    elif "notepad" in command:
        speak("Opening Notepad sir")
        Automation.open_notepad()
        current_app = "notepad"

    # -------------------------------
    # CALCULATOR
    # -------------------------------
    elif "calculator" in command or "calc" in command:
        speak("Opening Calculator sir")
        Automation.open_calculator()

    # -------------------------------
    # SCREENSHOT
    # -------------------------------
    elif "screenshot" in command:
        speak("Taking screenshot sir")
        Automation.take_screenshot()
        speak("Screenshot saved sir")

    # -------------------------------
    # CLOSE WINDOW
    # -------------------------------
    elif "close window" in command:
        speak("Closing current window sir")
        Automation.close_window()

    # -------------------------------
    # SWITCH WINDOW
    # -------------------------------
    elif "switch window" in command:
        speak("Switching window sir")
        Automation.switch_window()

    # -------------------------------
    # SHOW DESKTOP
    # -------------------------------
    elif "desktop" in command:
        speak("Showing desktop sir")
        Automation.show_desktop()

    # -------------------------------
    # SEARCH IN CHROME
    # -------------------------------
    elif current_app == "chrome" and "search" in command:
        query = command.replace("search", "").strip()

        if query:
            speak("Searching sir")
            Automation.type_text(query)
            Automation.press_enter()

    # -------------------------------
    # WRITE IN NOTEPAD
    # -------------------------------
    elif current_app == "notepad" and "write" in command:
        text = command.replace("write", "").strip()

        if text:
            speak("Writing sir")
            Automation.type_text(text)

    # -------------------------------
    # EXIT
    # -------------------------------
    elif "exit" in command:
        speak("Goodbye Piyush sir")
        return False

    # -------------------------------
    # AI MODE
    # -------------------------------
    else:
        speak("Let me think sir")

        try:
            answer = ask_ai(command)

            if answer:
                speak(answer[:180])
            else:
                speak("I did not understand sir")

        except Exception as e:
            print("AI Error:", e)
            speak("System is busy sir")

    return True


# ==========================================
# MAIN LOOP
# ==========================================
def run_assistant():
    speak("Hello Piyush sir. NeuroDesk AI is ready for your command.")

    running = True

    while running:

        command = listen()

        if command:
            print("Processing:", command)
            running = process_command(command)

        time.sleep(0.2)


# ==========================================
# RUN DIRECTLY
# ==========================================
if __name__ == "__main__":
    run_assistant()