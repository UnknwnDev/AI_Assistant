from pyowm import OWM
from geopy import Nominatim
from datetime import datetime

class Weather():

	# The location of where we want the forecast for
	__location = "Federal Way, US"

	# API Key
	api_key = "20dbe2afc5e93931d55bb2baa512cd84"

	def __init__(self):
		self.ow = OWM(self.api_key)
		self.mgr = self.ow.weather_manager()
		locator = Nominatim(user_agent="myGeocoder")
		city = "Federal Way"
		county = "US"
		self.__location = city + ", " + county
		loc = locator.geocode(self.__location)
		self.lat = loc.latitude
		self.long = loc.longitude

	@property
	def weather(self):
		forcast = self.mgr.one_call(lat=self.lat, lon=self.long)
		return forcast

# Demo
myweather = Weather()
print(myweather.weather)