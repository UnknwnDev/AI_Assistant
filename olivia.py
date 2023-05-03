# Name of Virtual Assistant: OLIVIA - Organic Learning and Interactive Virtual Intelligence Assistant
# TODO: Renname file later
from Voice_Recognition.ai import AI

olivia = AI('Olivia')

command = ""
current_tag = None

while True and current_tag != "exit":
	try:
		command = olivia.listen()
		command = command.lower()
		olivia.say(olivia.assistant.request(command))
		current_tag = olivia.assistant.request_tag(command)
	except:
		print("There was an error")
		command = ""
	print("Command was:", command)
	if current_tag is not None:
		if current_tag == "add_todo":
			olivia.skills.add_todo()
		if current_tag == 'show_todos':
			olivia.skills.show_todos()
		if current_tag == 'remove_todo':
			olivia.skills.remove_todo()

		current_tag = None
	
