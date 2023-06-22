import os
import sys
import json
import playsound
import speech_recognition as sr
# from TTS.api import TTS
from transformers import pipeline
from eventhook import Event_hook
from threading import Thread, Lock
from time import sleep
import error_fix

"""
	NOTE: Change this later to use NLP and RNN
"""

class AI:
	__name = ""
	lock = Lock()

	def __init__(self, name=None, new_flag = False):
		#print(sr.Microphone.list_microphone_names())
		self.classifier = pipeline("zero-shot-classification", )
		self.command_labels = ["greeting", "jokes", "facts", "insult", "add todo", "remove todo", "show todos", "add event", "remove event", "list events", "say", "wiki", "exit"]  # All commands
		self.labels = ["command", "conversation"]
		# self.tts = TTS("tts_models/en/jenny/jenny")


		# model = Model("./model") # path to model
		self.r = sr.Recognizer()

		# info = self.m.get_host_api_info_by_index(0)
		# numdevices = info.get('deviceCount')

		# for i in range(0, numdevices):
		# 		if (self.m.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
		# 				print("Input Device id ", i, " - ", self.m.get_device_info_by_host_api_device_index(0, i).get('name'))
		# Setup event hooks

		self.before_speaking = Event_hook()
		self.after_speaking = Event_hook()
		self.before_listening = Event_hook()
		self.after_listening = Event_hook()

	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self, value):
		sentence = f"Hello, my name is {self.__name}"
		self.__name = value
		self.say(sentence)
	
	def speak(self, sentence):
		if sentence == "":
			sentence = "Sorry I didn't catch that."
		# tts.tts_to_file(text=sentence, file_path="./out", emotion="Happy", speed=3.5)
		
		self.lock.acquire()
		
		# webfile = "web.mp3"
		# tts.save(webfile)
		self.before_speaking.trigger(sentence)
		# filename = "out"
		# tts.save(filename)
		
		# playsound.playsound(filename)
		# os.remove(filename)

		
		self.after_speaking.trigger(sentence)

		self.lock.release()
		

	def say(self, sentence: str):
		""" launch a new thread to speak """
		t = Thread(target = self.speak, args = (sentence,))
		t.start()
		t.join()

	def listen(self):
		
		phrase = ""

		while True:
			try:
				with sr.Microphone() as source:
					self.r.adjust_for_ambient_noise(source, duration=0.2)

					audio = self.r.listen(source)

					phrase = self.r.recognize_google(audio)
					phrase = phrase.lower()
					return phrase

			except sr.RequestError as e:
				print("Could not request reults; {0}".format(e))
				return None

			except sr.UnknownValueError:
				print("unknwn error occured")
				return None


		

	def process(self, message: str, flag):
		original = message.lower()
		tag = ''
		command = ''
		new = ''
		label, score = self.classify_sentence(message, flag)
		print(f"Label: {label}")
		print(f"Score: {score}")

		# if self.name.lower() in original:  # TODO: When Olivia is called start parsing text for command and tag
		# 	new = original[original.find(self.name.lower()) + len(self.name.lower()):]
		# 	new = new.replace(' ', '', 1) if new[0] == ' ' else new
		# 	print(new)
		# 	print(self.assistant.request(new))
		# 	print(self.assistant._predict_class(new))
		return label
	
	def classify_sentence(self, sentence, flag):
		print("="*17 + "classify_sentence" + "="*16)
		result = self.classifier(sentence, self.labels)
		label = result["labels"][0]
		score = result["scores"][0]

		print("Initial: " +label)
		print("Initial: " +str(score))

		if "command" in label and flag:
			result = self.classifier(sentence, self.command_labels, multi_label=True)

			label = result["labels"][0]
			score = result["scores"][0]

			print("Command: " +label)
			print("Command: " +str(score))


		print("="*50)
		return label, score
				

'''
TODO:
1. Find a way to remove words before and also name example "This is random Olivia Say Hello" -> "Say Hello"
2. Find a way to seperate taged commands with custom responses.
3. Return tag and command 
'''