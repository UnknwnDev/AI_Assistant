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
		ai.say(new)


def initialize():
	factory.register('say_skill', SaySkill)
	# print("goodday initialized")