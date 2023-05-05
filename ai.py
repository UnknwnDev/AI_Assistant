import os
import sys
import json
import playsound
from pyaudio import PyAudio, paInt16
import error_fix
from gtts import gTTS 
from neuralintents import GenericAssistant
from vosk import Model, KaldiRecognizer
from eventhook import Event_hook
from threading import Thread, Lock
from time import sleep


"""
	NOTE: Change this later to use NLP and RNN
"""

class AI:
	__name = ""
	lock = Lock()

	def __init__(self, name=None, new_flag = False):
		#print(sr.Microphone.list_microphone_names())


		model = Model("./model") # path to model
		self.r = KaldiRecognizer(model, 44100)

		self.m = PyAudio()

		# info = self.m.get_host_api_info_by_index(0)
		# numdevices = info.get('deviceCount')

		# for i in range(0, numdevices):
		# 		if (self.m.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
		# 				print("Input Device id ", i, " - ", self.m.get_device_info_by_host_api_device_index(0, i).get('name'))

		self.assistant = GenericAssistant('data/intents.json')
		if name is not None:
			self.__name = name
			if new_flag:
				self.__update()
			else:
				self.assistant.load_model(self.name)

		self.audio = self.m.open(format=paInt16, channels=1,rate=44100, input=True, frames_per_buffer=8192, input_device_index=5)
		self.audio.start_stream()

		# Setup event hooks
		self.before_speaking = Event_hook()
		self.after_speaking = Event_hook()
		self.before_listening = Event_hook()
		self.after_listening = Event_hook()

	def __update(self):
		self.assistant.train_model()
		self.assistant.save_model(self.name)

	@property
	def name(self):
		return self.__name
	
	@name.setter
	def name(self, value):
		sentence = f"Hello, my name is {self.__name}"
		self.__name = value
		self.say(sentence)
	
	def speak(self, sentence):
		print(sentence)
		tts = gTTS(text=sentence, lang='en', tld='com.au')
		
		self.lock.acquire()
		self.before_speaking.trigger(sentence)
		filename = "out"
		tts.save(filename)
		playsound.playsound(filename)
		os.remove(filename)
		self.after_speaking.trigger(sentence)

		self.lock.release()
		

	def say(self, sentence: str):
		""" launch a new thread to speak """
		t = Thread(target = self.speak, args = (sentence,))
		t.start()
		t.join()

	def listen(self):
		
		phrase = ""
		
		while not os._exists("out"):
			
			if self.r.AcceptWaveform(self.audio.read(4096, exception_on_overflow=False)):
				self.before_listening.trigger()
				phrase = self.r.Result()
				#phrase = phrase.removeprefix('the')

				phrase = str(json.loads(phrase)['text'])

				if phrase:
					self.after_listening.trigger(phrase)
				return phrase

		return None



