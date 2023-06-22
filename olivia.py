# Name of Virtual Assistant: OLIVIA - Organic Learning and Interactive Virtual Intelligence Assistant
from ai import AI
from datetime import datetime
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook
import sys
import os
from time import sleep
from chatbot import ChatBot

olivia = AI('Olivia')
olivia_chat = ChatBot()

olivia.start = Event_hook()
olivia.stop = Event_hook()

with open("skills/skills.json") as f:
	data = json.load(f)

	loader.load_skills(data['plugins'])

skills = [factory.create(item) for item in data['skills']]
print(f'skills: {skills}')

# Load the plugins
with open("./plugins/plugins.json") as f:
    plugin_data = json.load(f)
    print(f'plugins: {plugin_data["plugins"]}')
    # load the plugins
    plugin_loader.load_plugins(plugin_data["plugins"])

plugins = [plugin_factory.create(item) for item in plugin_data["items"]]

# Register all the plugins
for item in plugins:
    item.register(olivia)


activated_flag = False # Activates the olivia when name called

olivia.start.trigger()
current_tag = None
command = ""

name = "Olivia"


while True:
	command = ""
	label = ''
	
	while os.path.exists('web.mp3'):
		continue

	command = olivia.listen()
	current_tag = None


	if command:
		print(f'command heard: {command}')
		command = command.lower()
		label = olivia.process(command, activated_flag)
	
		if not activated_flag and name.lower() in command:
			olivia.say("Hello Sam, how may I help you?")
			activated_flag = True
		elif activated_flag and "exit" in label:
			olivia.say("Goodbye Sam, see you later.")
			activated_flag = False

		if activated_flag:
			# if "conversation" in label:
			olivia_chat.chat(command, olivia)
			# else:
			# 	for skill in skills:
			# 		if label in skill.commands(label):
			# 			skill.handle_command(label, olivia)


		# if 'command' in label:
		# 	# if message != "":
		# 	# 	olivia.say(message)
		# 	if name.lower() in command:
		# 		for skill in skills:
		# 			if current_tag in skill.commands(current_tag):
		# 				skill.handle_command(current_tag, olivia)

