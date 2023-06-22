from dataclasses import dataclass
from skills import factory
from ai import AI

@dataclass
class SaySkill:
	name = 'say_skill'

	def commands(self, command:str):
		return 'say'
	
	def handle_command(self, command:str, ai:AI):
		new = ai.listen()
		if new is not None:
			ai.say(new)
		else:
			ai.say("Sorry I didn't catch that.")


def initialize():
	factory.register('say_skill', SaySkill)
	# print("goodday initialized")