from dataclasses import dataclass
from ai import AI
import plugins.plugin_factory
from flask import Flask, Response, render_template, json
from flask_cors import CORS
import logging
from threading import Thread
import os
from time import sleep

@dataclass
class Audio_Stream_Plugin:
	name = 'conversation_history'
	app = Flask(__name__)

	def __init__(self):
		CORS(self.app)
		self.app.add_url_rule('/mp3', 'audio_streaming', self.streammp3)
		self.app.add_url_rule('/play_sound', 'sound', self.play_sound)
		self.app.add_url_rule('/delete_sound', 'delete_sound', self.delete_sound)
		logging.getLogger('werkzeug').disabled = True

	def play_sound(self):
		if os.path.exists('web.mp3'):
			return json.jsonify({ 'flag': "True" }) 
		else:
			return json.jsonify({ 'flag': "False" }) 

	def delete_sound(self):
		if os.path.exists('web.mp3'):
			os.remove('web.mp3')
			return json.jsonify(result="True")
		return json.jsonify(result="False")

	def streammp3(self):
			def generate():
					if os.path.exists('web.mp3'):
						with open("web.mp3", "rb") as fwav:
							data = fwav.read(1024)
							while data:
									yield data
									data = fwav.read(1024)
			return Response(generate(), mimetype="audio/mpeg")

	def start_flask_thread(self):
		""" Start flask thread """
		print("starting api thread")
		

	def start(self):
		print("starting API server")
		self.flask = Thread(target=self.app.run, kwargs={
            'host': '0.0.0.0',
            'port': 5000,
            'use_reloader': False,
            'threaded': True,
						'debug': True
        })
		self.flask.start()
		return self

	def stop(self):
		# shutdown the flask server
		print("stopping api server")
		self.flask.join()

	def register(self, ai:AI):
		self.ai = ai
		self.ai.start.register(self.start)  
		self.ai.stop.register(self.stop)
		return self


def initialize():
    # register with Factory or plugin?
    plugins.plugin_factory.register('audio_stream_plugin', Audio_Stream_Plugin)	