import time
import os
from pynput import keyboard
from pynput.keyboard import Controller, Key
from modules.manager import TriggerManager

ctrl = Controller()
tm = TriggerManager()

current_word = ""
last_modified = os.getmtime(tm.trigger_file) if os.path.exists(tm.trigger_file) else 0

def check_for_updates():
    global last_modified
    if os.path.exists(tm.trigger_file):
        current_mtime = os.path.getmtime(tm.trigger_file)
        if current_mtime != last_modified:
            tm.reload_trigs()
            last_modified = current_mtime
            print("[System] Triggers reloaded")

def expand_text(trigger, expansion, end_key):
    for _ in range(len(trigger) + 1):
        ctrl.press(Key.backspace)
        ctrl.release(Key.backspace)

    time.sleep(0.03)

    ctrl.type(expansion)

    ctrl.press(end_key)
    ctrl.release(end_key)

def on_press(key):
    global current_word

    try:
        if key in (Key.space, Key.enter):
            check_for_updates()

            if tm.check_trig(current_word):
                expansion = tm.get_trig(current_word)
                print(f"[Expand] '{current_word}' -> '{expansion}'")
                expand_text(current_word, expansion, key)

            current_word = ""

        elif key == Key.backspace:
            current_word = current_word[:-1]

        elif key in (Key.esc, Key.tab, Key.enter, Key.up, Key.down, Key.up, Key.left, Key.right):
            current_word = ""

        elif hasattr(key, "char") and key.char is not None:
            current_word += key.char

    except Exception as e:
        print(f"[Error] {e}")
        current_word = ""

if __name__ == "__main__":
    print("Kae Running... \n Press Ctrl+C to stop")
    tm.list_trigs()

    with keyboard.Listener(on_press==on_press) as listener:
        listener.join()