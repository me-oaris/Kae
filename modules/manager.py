import json
import os

class TriggerManager:
    def __init__(self, trigger_file="triggers.json"):
        self.trigger_file = trigger_file
        self.triggers = self.load_trigs()

    def load_trigs(self):
        if os.path.exists(self.trigger_file):
            with open(self.trigger_file, "r") as file:
                return json.load(file)
        else:
            return {}

    def reload_trigs(self):
        self.triggers = self.load_trigs()

    def save_trigs(self):
        with open(self.trigger_file, "w") as file:
            json.dump(self.triggers, file, indent=4)

    def add_trig(self, trigger, expansion):
        self.triggers[trigger] = expansion
        self.save_trigs()

    def remove_trig(self, trigger):
        if trigger in self.triggers:
            del self.triggers[trigger]
            self.save_trigs()

    def get_trig(self, trigger):
        return self.triggers.get(trigger, None)

    def list_trigs(self):
        if not self.triggers:
            print("No triggers found.")
        else:
            for trigger, expansion in self.triggers.items():
                print(f"{trigger}: {expansion}")

    def check_trig(self, trigger):
        return trigger in self.triggers