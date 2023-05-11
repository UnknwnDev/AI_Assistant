from ics import Calendar, Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
from dataclasses import dataclass
import dateparser
from skills import factory
from ai import AI

calender_filename = 'docs/myfile.ics'
calender_datafile = 'data/myfile.yml'


class Calendar_for_AI():
	c = Calendar()

	def __init__(self):
		''' Print a nice banner '''
		print("")
		print("*"*50)
		print("Calender Skill Loaded")
		print("*"*50)
	
	def add_event(self, begin:str, name:str, description:str=None) -> bool:
		''' adds an even to calender '''
		e = Event()
		e.name = name
		e.begin = begin # format should be = '2023-05-03 19:30:00'
		e.description = description
		try:
			self.c.events.add(e)
			return True
		except:
			print("There was a problemm add the event , sorry.")
			return False

	def remove_event(self, event_name:str):
		''' Removes the event from the calender '''

		# find the event
		for event in self.c.events:
			if event.name.lower() == event_name.lower():
				# found it
				self.c.events.remove(event)
				print("Removing event:", event_name)
				return True

		# not found
		print("Sorry could not find that event:", event_name)
		return False
	
	def parse_to_dict(self):
		dict = []
		for event in self.c.events:
			my_event = {}
			my_event['begin'] = event.begin.datetime
			my_event['name'] = event.name
			my_event['description'] = event.description
			dict.append(my_event)
			# print('parsing file:', yaml.dump(dict, default_flow_style=False))
		return dict

	def save(self):
		# Save the Calender ICS file
		with open(calender_filename, 'w') as my_file:
			my_file.writelines(self.c)
		# Save to YAML Data file

		# first check that there are some entries in the dictionary, otherwise remove the first file
		if self.c.events == set():
			print("No Events - Removing YAML file")
			try:
				os.remove(calender_datafile)
			except:
				print("Oops cound'nt delet the YAML file")
		else:
			with open(calender_datafile,'w') as outfile:

				yaml.dump(self.parse_to_dict(), outfile, default_flow_style=False)

	def load(self):
		''' load the Calender data from the YAML file '''
		filename = calender_datafile
		my_file = Path(filename)

		# Check if the file exists
		if my_file.is_file():
			stream = open(filename,'r')
			event_list = yaml.load(stream, Loader=yaml.Loader)
			for item in event_list:
				e = Event()
				e.begin = item['begin']
				e.description = item['description']
				e.name = item['name']
				self.c.events.add(e)
		else:
			# file doesn't exist
			print("File does not exist")
	
	def list_events(self, period:str=None) -> bool:
		''' Lists the upcoming events
		if `period` is left empty it will default to today
		other options are:
		`all` - lists all events in the calender
		`this week` - lists all the events this week
		`this month` - lists all the events this month
		'''

		if period == None:
			period = "this week"
		
		# Check that there are events
		if self.c.events == set():
			# No events found
			print("No Events in Calender")
			return None
		else:
			event_list = []
			# have to fix localization - that the +00 timezone bit on the date
			# otherwise it complains of non-naive date being compared to naive date
			now = pytz.utc.localize(datetime.now())
			if period == "this week":
				nextperiod = now+relativedelta(weeks=+1)
			if period == "this month":
				nextperiod = now+relativedelta(months=+1)
			if period == "all":
				nextperiod = now+relativedelta(years=+100)
			for event in self.c.events:
				event_date = event.begin.datetime
				if (event_date >= now) and (event_date <= nextperiod):
					event_list.append(event)
			
			return event_list

@dataclass
class Calender_skill():
	name = 'calendar_skill'
	calendar = Calendar_for_AI()
	calendar.load()

	def commands(self, command:str):
			return ['add_event', 'remove_event', 'list_events']

	def add_event(self, olivia:AI) -> bool:
		try:
			event_name = olivia.listen()
			olivia.say("When is this event?")
			event_begin = olivia.listen()
			event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
			olivia.say("What is the event description?")
			event_description = olivia.listen()
			message = f"Ok, adding event {event_name}"
			olivia.say(message)
			self.calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
			self.calendar.save()
			return True
		except:
			print("Oops there was an error")
			return False

	def remove_event(self, olivia:AI) -> bool:
		try:
			event_name = olivia.listen()
			try:
				self.calendar.remove_event(event_name=event_name)
				olivia.say("Event removed successfully")
				self.calendar.save()
				return True
			except:
				olivia.say("Sorry I could not find the event", event_name)
				return False
		except:
			print("Oops there was an error")
			return False

	def list_events(self, period, olivia:AI):
		this_period = self.calendar.list_events(period=period)
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
			message = message + " in the diary"
			# print(message)
			olivia.say(message)
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
				olivia.say(message)
		else:
			olivia.say("There are no events in the calender!")

	def handle_command(self, command:str, ai:AI):
		
		if command in 'add_event':
				self.add_event(olivia=ai)
		if command in 'remove_event':
				self.remove_event(olivia=ai)
		if command in 'list_events':
				self.list_events(period='this month', olivia=ai)
			

def initialize():
    factory.register('calendar_skill', Calender_skill)