from time import sleep
from eventhook import Event_hook

def test_event_hook_after():
	print("This is an event hook for after")

def test_event_hook_before():
	print("This is an event hook for befor")

def moosay():
	print("This is a moosay")

before = Event_hook()
after = Event_hook()

before.register(test_event_hook_before)
after.register(test_event_hook_after)
after.register(moosay)

while True:
	
	before.trigger()
	print("loop de loop")
	after.trigger()
	print("")
	print("*"*20)
	print("")
	sleep(1)