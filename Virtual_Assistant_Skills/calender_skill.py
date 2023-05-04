import os
import yaml
import pytz
from pathlib import Path
from datetime import datetime
from ics import Calendar, Event
from dateutil.relativedelta import *

calender_filename = 'docs/myfile.ics'
calender_datafile = 'Virtual_Assistant_Skills/data/myfile.yml'


class Calendar_Skill():
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
			if event.name == event_name:
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
			event_list = yaml.load(stream)
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
			now = pytz.utc.localize(datetime.utcnow())
			now = now.astimezone(pytz.timezone('US/Pacific'))
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

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cal = Calendar_Skill()
cal.add_event(time, "Test", "math-140 test")
cal.add_event(time, "Other", "math-140 test")
cal.save()
cal.list_events()
