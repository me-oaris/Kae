from pynput import keyboard
from pynput.keyboard import Controller
import json
import time

keyController = Controller()
phrase = ""

def load_triggers():
        with open("triggers.json", "r") as file:
            return json.load(file)

triggers = load_triggers()

def click(key):
    keyController.press(key)
    keyController.release(key)

def trigger_expand(trig,action):
    if trig in triggers:
        print(f"Found! Expanding {trig} to {triggers[trig]}")
        keyController.press(keyboard.Key.shift)
        for _ in range(len(trig) + 1):
            click(keyboard.Key.left)
        keyController.release(keyboard.Key.shift)
        keyController.press(keyboard.Key.backspace)
        keyController.release(keyboard.Key.backspace)

        time.sleep(0.1)  # Here, small fix for the deletion issue

        keyController.type(triggers[trig])
        print(f"Expanded {trig} to {triggers[trig]}")
        click(action)
    else:
        print(f"No trigger found for {trig}")

def on_type(key):
    global phrase
    try:
        if key == keyboard.Key.space or key == keyboard.Key.enter:
            if phrase.startswith("!"):
                print("Trigger Detected")
                print(f"Action: {key}")
                trigger_expand(phrase,key)
                phrase = ""
            else:
                print(f"Typed phrase: {phrase}")
                phrase = ""
        elif key == keyboard.Key.backspace:
            phrase = phrase[:-1]
        else:
            phrase += key.char
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_type)
listener.start()
listener.join()
