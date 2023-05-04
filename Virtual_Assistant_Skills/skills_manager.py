import pyjokes
import dateparser
from Virtual_Assistant_Skills.calender_skill import Calendar_Skill
from Virtual_Assistant_Skills.Notes_and_Todos.todo_list import Todo, Item

class Skills:
	__todo = Todo()
	__ai = None
	__calender = Calendar_Skill()
	def __init__(self, ai):
		self.__ai = ai
		self.__calender.load()

	def jokes(self):
		funny = pyjokes.get_joke()
		print(funny)
		self.__ai.say(funny)

#########################TODO############################
	def add_todo(self) -> bool:
		item = Item()
		try:
			item.title = self.__ai.listen()
			self.__todo.new_item(item)
			message = f"Added {item.title}"
			self.__ai.say(message)
			return True
		except:
			print("There was an error")
			return False
	
	def show_todos(self):
		was_empty: bool = True
		if len(self.__todo) > 0:
			for item in self.__todo:
				self.__ai.say(item.title)
				was_empty = False
			else:
				if was_empty:
					self.__ai.say("The list appears to be empty!")
				else:
					self.__ai.say("The list is empty!")

	def remove_todo(self) -> bool:
		try:
			item_title = self.__ai.listen()
			self.__todo.remove_item(title = item_title)
			message = f"Removed {item_title}"
			self.__ai.say(message)
			return True
		except:
			print("There was an error")
			return False
#########################Calender############################
	def add_event(self) -> bool:
		try:
			event_name = self.__ai.listen()
			self.__ai.say("When is this event?")
			event_begin = self.__ai.listen()
			event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
			self.__ai.say("What is the event description?")
			event_description = self.__ai.listen()
			message = f"Ok, adding event {event_name}"
			self.__ai.say(message)
			self.__calender.add_event(begin=event_begin, name=event_name, description=event_description)
			self.__calender.save()
			return True
		except:
			print("Opps there was an error")
			return False
	
	def remove_event() -> bool:
		try:
			event_name = self.__ai.listen()
			try:
				self.__calender.remove_event(event_name=event_name)
				self.__ai.say("Event removed successfully")
				self.__calender.save()
				return True
			except:
				self.__ai.say("Sorry I could not find the event", event_name)
				return False
		except:
			print("Oops ther was an error")
			return False