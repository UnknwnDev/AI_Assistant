class Event_hook:

	handlers = []
	

	def __init__(self):
		self.handlers = []

	
	def register(self, handler):
		print('Registering event hook')
		self.handlers.append(handler)
		return self
	
	def unregister(self, handler):
		print('Unregistering event hook')
		self.handlers.remove(handler)
		return self
	
	def trigger(self, *args, **kwargs):
		for handler in self.handlers:
			handler(*args, **kwargs)
