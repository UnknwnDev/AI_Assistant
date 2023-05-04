import os
import sys
import playsound
import Voice_Recognition.error_fix
from gtts import gTTS 
import speech_recognition as sr
from neuralintents import GenericAssistant
sys.path.append('./')
from Virtual_Assistant_Skills.skills_manager import Skills

"""
	NOTE: Change this later to use NLP and RNN
"""

class AI:
	__name = ""
	def __init__(self, name=None, new_flag = False):
		self.r = sr.Recognizer()
		self.m = sr.Microphone()

		#print(sr.Microphone.list_microphone_names())

		self.skills = Skills(self)

		self.assistant = GenericAssistant('Voice_Recognition/intents.json')
		if name is not None:
			self.__name = name
			if new_flag:
				self.__update()
			else:
				self.assistant.load_model(self.name)

		
		print("Listening")
		with self.m as source:
			self.r.adjust_for_ambient_noise(source, duration=0.5)

	def __update(self):
		self.assistant.train_model()
		self.assistant.save_model(self.name)

	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self, value):
		scentence = f"Hello, my name is {self.__name}"
		self.__name = value
		self.say(scentence)
	
	def say(self, scentence: str):
		tts = gTTS(text=scentence, lang='en', tld='com.au')

		filename = "out"
		tts.save(filename)
		playsound.playsound(filename)
		os.remove(filename)


	def listen(self):
		print("Say something")
		with self.m as source:
			self.r.adjust_for_ambient_noise(source, duration=0.5)
			audio = self.r.listen(source)
			print("Got it")

		try:
			phrase = self.r.recognize_google(audio, show_all=False, language='en')
			#scentence = f"Got it, you said {phrase}"
			#self.say(scentence)
			print("You said", phrase)
			return phrase
		except sr.UnknownValueError as e:
			print("Sorry, didn't catch that", e)
			self.say("Sorry didn't catch that")



