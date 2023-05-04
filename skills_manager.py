import pyjokes
import dateparser
from skills.calender import Calendar_Skill
from skills.todo import Todo, Item

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
			self.__calender.add_event(begin=event_isodate, name=event_name, description=event_description)
			self.__calender.save()
			return True
		except:
			print("Oops there was an error")
			return False
	
	def remove_event(self) -> bool:
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
			print("Oops there was an error")
			return False

	def list_events(self, period):
		this_period = self.__calender.list_events(period=period)
		if this_period is not None:
			message = "There "
			if len(this_period) > 1:
				message = message + 'are '
			else:
				message = message + 'is '
			message = message + str(len(this_period))
			if len(this_period) > 1:
				message = message + ' events'
			else:
				message = message + ' event'
			message = message + " in the dairy"
			# print(message)
			self.__ai.say(message)
			for event in this_period:
				event_date = event.begin.datetime
				weekday = datetime.strftime(event_date, "%A")
				day = str(event.begin.datetime.day)
				month = datetime.strftime(event_date, "%B")
				year = datetime.strftime(event_date, "%Y")
				time = datetime.strftime(event_date, "%I:%M %p")
				name = event.name
				description = event.description
				message = f"On {weekday} {day} of {month} {year} at {time}"
				message = f"{message}, there is an event called {name}"
				message = f"{message} with an event description of {description}"
				# print(message)
				self.__ai.say(message)
				
