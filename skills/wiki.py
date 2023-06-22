from dataclasses import dataclass
from skills import factory
from ai import AI
from wikipediaapi import Wikipedia
from debug import printf

class Wiki:
	def __init__(self):
		self.result = []
		self.wiki = Wikipedia('en')

	def search(self, query: str, ai:AI):
		self.result = self.wiki.page(query).summary

		printf("Wiki Search", self.result)

		if not self.result:
			return "No results found."
		return self.result



@dataclass
class WikiSkill:
	name = 'wiki_skill'

	def commands(self, command:str):
		return 'wiki'
	
	def handle_command(self, command:str, ai:AI):
		ai.say("What do you want me to search for you?")
		new = ai.listen()
		if new is not None and new != '':
			ai.say(Wiki().search("Backrooms", ai))
		else:
			ai.say("Sorry I didn't catch that.")


def initialize():
	factory.register('wiki_skill', WikiSkill)
	# print("goodday initialized")
