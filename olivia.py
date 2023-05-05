# Name of Virtual Assistant: OLIVIA - Organic Learning and Interactive Virtual Intelligence Assistant
from ai import AI
from datetime import datetime
from skills import factory, loader
from plugins import plugin_loader, plugin_factory
import json
from eventhook import Event_hook
import sys


olivia = AI('Olivia')

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




olivia.start.trigger()
current_tag = None
command = ""

while True and command not in ['good bye', 'bye', 'quit', 'exit', 'goodbye', 'the exit']:
	command = ""
	command = olivia.listen()
	current_tag = None

	if command:
		print(f'command heard: {command}')
		command = command.lower()
		olivia.say(olivia.assistant.request(command))
		current_tag = olivia.assistant.request_tag(command)

		for skill in skills:
			if current_tag in skill.commands(current_tag):
				skill.handle_command(current_tag, olivia)
