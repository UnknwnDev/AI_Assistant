# Name of Virtual Assistant: OLIVIA - Organic Learning and Interactive Virtual Intelligence Assistant
# TODO: Renname file later
from ai import AI

olivia = AI('Olivia')

command = ""
current_tag = None

while True:
	try:
		command = olivia.listen()
		command = command.lower()
		olivia.say(olivia.assistant.request(command))
		current_tag = olivia.assistant.request_tag(command)
	except:
		print("There was an error")
		command = ""
	print("Command was:", command)

	#####################################
	if current_tag is not None:
		print("Tag was:", current_tag)
		#********************************#
		if current_tag == "add_todo":
			olivia.skills.add_todo()
		if current_tag == 'show_todos':
			olivia.skills.show_todos()
		if current_tag == 'remove_todo':
			olivia.skills.remove_todo()
		#********************************#
		if current_tag == "jokes":
			olivia.skills.jokes()
		#********************************#
		if current_tag == "add_event":
			olivia.skills.add_event()
		if current_tag == 'list_events':
			olivia.skills.list_events()
		if current_tag == 'remove_event':
			olivia.skills.remove_event()
		#********************************#

		if current_tag == "exit":
			break

		current_tag = None
	######################################
