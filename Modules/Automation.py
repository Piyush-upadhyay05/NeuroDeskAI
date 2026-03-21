import pyautogui
import os
import time

# ------------------------
# Application Control
# ------------------------

def open_chrome():
    os.system("start chrome")

def open_notepad():
    os.system("notepad")

def open_calculator():
    os.system("calc")


# ------------------------
# Desktop Control
# ------------------------

def show_desktop():
    pyautogui.hotkey("win", "d")

def switch_window():
    pyautogui.hotkey("alt", "tab")

def close_window():
    pyautogui.hotkey("alt", "f4")


# ------------------------
# Screenshot
# ------------------------

def take_screenshot():
    file = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot(file)
    return file


# ------------------------
# Folder Opening
# ------------------------

def open_folder(folder):

    paths = {
        "documents": "C:\\Users\\LENOVO\\Documents",
        "downloads": "C:\\Users\\LENOVO\\Downloads",
        "desktop": "C:\\Users\\LENOVO\\Desktop"
    }

    if folder in paths:
        os.startfile(paths[folder])


# ------------------------
# Search Folder in PC
# ------------------------

def search_folder(name):

    base = "C:\\Users\\LENOVO"

    for root, dirs, files in os.walk(base):
        for d in dirs:
            if name.lower() in d.lower():
                os.startfile(os.path.join(root, d))
                return True

    return False
def type_text(text):
    pyautogui.write(text, interval=0.05)

def press_enter():
    pyautogui.press("enter")

def hotkey(k1, k2):
    pyautogui.hotkey(k1, k2)

def scroll_down():
    pyautogui.scroll(-500)

def scroll_up():
    pyautogui.scroll(500)