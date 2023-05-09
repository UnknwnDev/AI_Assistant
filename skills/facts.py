from randfacts import randfacts
from dataclasses import dataclass
from skills import factory
from ai import AI

@dataclass
class Facts_skill():
	name = 'facts_skill'

	def commands(self, command:str):
		return 'facts'
	
	def handle_command(self, command:str, ai:AI):
		fact = randfacts.get_fact()
		ai.say(fact)
		return fact


def initialize():
	factory.register('facts_skill', Facts_skill)
	# print("Facts Skill initialized")