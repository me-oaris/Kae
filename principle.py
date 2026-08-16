from pynput import keyboard
from pynput.keyboard import Controller
import time

keyController = Controller()
phrase = ""
trigger = "!name"
trigger_ans = "Lucian"

def trigger_expand(trig):
    if trig == trigger:
        for _ in range(len(trig) + 1):
            keyController.press(keyboard.Key.backspace)
            keyController   .release(keyboard.Key.backspace)
        time.sleep(0.1)
        keyController.type(trigger_ans + " ")

def on_type(key):
    global phrase
    try:
        if key == keyboard.Key.space:
            if phrase.startswith("!"):
                print("Trigger Detected")
                trigger_expand(phrase)
            else:
                print(f"Typed phrase: {phrase}")
                phrase = ""
        elif key == keyboard.Key.backspace:
            phrase = phrase[:-1]
        elif key == keyboard.Key.enter:
            phrase = ""
        else:
            phrase += key.char
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_type)
listener.start()
listener.join()
