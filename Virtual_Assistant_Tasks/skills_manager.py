import pyjokes
from Virtual_Assistant_Tasks.Notes_and_Todos.todo_list import Todo, Item

class Skills:
	__todo = Todo()
	__ai = None
	def __init__(self, ai):
		self.__ai = ai

	def joke(self):
		funny = pyjokes.get_joke()
		print(funny)
		self.__ai.say(funny)

#########################TODO############################
	def add_todo(self) -> bool:
		item = Item()
		try:
			item.title = self.__ai.listen()
			self.__todo.new_item(item)
			message = f"Added {item.title}"
			self.__ai.say(message)
			return True
		except:
			print("There was an error")
			return False
	
	def show_todos(self):
		was_empty: bool = True
		if len(self.__todo) > 0:
			for item in self.__todo:
				self.__ai.say(item.title)
				was_empty = False
			else:
				if was_empty:
					self.__ai.say("The list appears to be empty!")
				else:
					self.__ai.say("The list is empty!")

	def remove_todo(self) -> bool:
		try:
			item_title = self.__ai.listen()
			self.__todo.remove_item(title = item_title)
			message = f"Removed {item_title}"
			self.__ai.say(message)
			return True
		except:
			print("There was an error")
			return False
#########################____############################