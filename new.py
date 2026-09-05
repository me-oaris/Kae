from modules.manager import TriggerManager

tm = TriggerManager()

tm.add_trig("!test", "This is a test trigger.")
tm.add_trig("#email", "This is an email trigger.")

tm.list_trigs()

print("Added triggers\n")

tm.remove_trig("!test")
tm.remove_trig("#email")

print("Triggers after removal:\n")

tm.list_trigs()



