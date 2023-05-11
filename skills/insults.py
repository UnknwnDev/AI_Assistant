from dataclasses import dataclass
from skills import factory
from ai import AI
from pyinsults import insults

@dataclass
class Insults_skill:
	name = 'insults'

	def commands(self, command:str):
		return 'insult'

	def handle_command(self, command:str, ai:AI):
		insult = insults.long_insult()
		ai.say(insult)

def initialize():
    factory.register('insult_skill', Insults_skill)

