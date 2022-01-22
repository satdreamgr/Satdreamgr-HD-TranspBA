# -*- coding: UTF-8 -*-
#
# Converter - MSNWeather
# Developer - Sirius
# Version 0.8
# Homepage - http://www.gisclub.tv
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from os import stat
from time import time

from Components.config import config
from Components.Console import Console
from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from Tools.Directories import fileExists
from lxml import objectify

weather_city = config.plugins.weathermsn.city.value
degreetype = config.plugins.weathermsn.degreetype.value
windtype = config.plugins.weathermsn.windtype.value
weather_location = config.osd.language.value.replace('_', '-')

if weather_location == 'en-EN':
	weather_location = 'en-US'

time_update = 20
time_update_ms = 3000


class TranspBAMSNWeather2(Converter, Poll):

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.iConsole = Console()
		self.poll_interval = time_update_ms
		self.poll_enabled = True

	def control_xml(self, result, retval, extra_args):
		if retval != 0:
			self.write_none()

	def write_none(self):
		with open("/tmp/weathermsn.xml", "w") as noneweather:
			noneweather.write("None")
		noneweather.close()

	def get_xmlfile(self):
		self.iConsole.ePopen("wget -P /tmp -T2 'http://weather.service.msn.com/data.aspx?weadegreetype=%s&culture=%s&weasearchstr=%s&src=outlook' -O /tmp/weathermsn.xml" % (degreetype, weather_location, weather_city), self.control_xml)

	@cached
	def getText(self):
		info, weze = 'n/a', ''
		msnweather = {'Vfd': '', 'Date': '', 'Shortdate': '', 'Day': '', 'Shortday': '',
			'Location': '', 'Timezone': '', 'Latitude': '', 'Longitude': '',
			'Temp': '', 'Picon': '', 'Skytext': '', 'Feelslike': '', 'Humidity': '', 'Wind': '', 'Windspeed': '',
			'Date0': '', 'Shortdate0': '', 'Day0': '', 'Shortday0': '', 'Temp0': '', 'Lowtemp0': '', 'Hightemp0': '', 'Picon0': '', 'Skytext0': '', 'Precip0': '',
			'Date1': '', 'Shortdate1': '', 'Day1': '', 'Shortday1': '', 'Temp1': '', 'Lowtemp1': '', 'Hightemp1': '', 'Picon1': '', 'Skytext1': '', 'Precip1': '',
			'Date2': '', 'Shortdate2': '', 'Day2': '', 'Shortday2': '', 'Temp2': '', 'Lowtemp2': '', 'Hightemp2': '', 'Picon2': '', 'Skytext2': '', 'Precip2': '',
			'Date3': '', 'Shortdate3': '', 'Day3': '', 'Shortday3': '', 'Temp3': '', 'Lowtemp3': '', 'Hightemp3': '', 'Picon3': '', 'Skytext3': '', 'Precip3': '',
			'Date4': '', 'Shortdate4': '', 'Day4': '', 'Shortday4': '', 'Temp4': '', 'Lowtemp4': '', 'Hightemp4': '', 'Picon4': '', 'Skytext4': '', 'Precip4': '',
			}
		low0weather, hi0weather, low1weather, hi1weather, low2weather, hi2weather, low3weather, hi3weather, low4weather, hi4weather = '', '', '', '', '', '', '', '', '', ''
		if fileExists("/tmp/weathermsn.xml"):
			if int((time() - stat("/tmp/weathermsn.xml").st_mtime) // 60) >= time_update:
				self.get_xmlfile()
		else:
			self.get_xmlfile()
		if not fileExists("/tmp/weathermsn.xml"):
			self.write_none()
			return info
		if fileExists("/tmp/weathermsn.xml") and open("/tmp/weathermsn.xml").read() == 'None':
			return info
		try:
			tree = objectify.fromstring(open("/tmp/weathermsn.xml").read())

			msnweather['Location'] = tree.weather.attrib['weatherlocationname'].split(',')[0]
			timezone = float(tree.weather.attrib['timezone'])
			msnweather['Timezone'] = '+' + tree.weather.attrib['timezone'] if timezone > 0 else tree.weather.attrib['timezone']
			msnweather['Latitude'] = latitude = tree.weather.attrib['lat'].replace(',', '.')
			msnweather['Longitude'] = longitude = tree.weather.attrib['long'].replace(',', '.')

			msnweather['Time'] = tree.weather.current.attrib['observationtime']
			msnweather['Point'] = tree.weather.current.attrib['observationpoint']
			msnweather['Attribution'] = tree.weather.attrib['attribution']

			temperature = float(tree.weather.current.attrib['temperature'])
			msnweather['Temperature'] = '+' + tree.weather.current.attrib['temperature'] if temperature > 0 else tree.weather.current.attrib['temperature']
			feelslike = float(tree.weather.current.attrib['feelslike'])
			msnweather['Feelslike'] = '+' + tree.weather.current.attrib['feelslike'] if feelslike > 0 else tree.weather.current.attrib['feelslike']
			msnweather['Picon'] = tree.weather.current.attrib['skycode']
			msnweather['Skytext'] = tree.weather.current.attrib['skytext']
			msnweather['Humidity'] = tree.weather.current.attrib['humidity']
			msnweather['Wind'] = tree.weather.current.attrib.get('winddisplay', '')

			_windspeed, _windtype = tree.weather.current.attrib.get('windspeed').split(' ')
			_windconv = {
				'ms_m/s': (1.0, _('%.01f ft/s')), 'ms_km/h': (0.28, _('%.01f ft/s')), 'ms_mph': (0.45, _('%.01f ft/s')),
				'fts_m/s': (3.28, _('%.01f mp/h')), 'fts_km/h': (0.91, _('%.01f mp/h')), 'fts_mph': (1.47, _('%.01f mp/h')),
				'mph_m/s': (2.24, _('%.01f mp/h')), 'mph_km/h': (0.62, _('%.01f mp/h')), 'mph_mph': (1.0, _('%.01f mp/h')),
				'knots_m/s': (1.94, _('%.01f knots')), 'knots_km/h': (0.54, _('%.01f knots')), 'knots_mph': (0.87, _('%.01f knots')),
				'kmh_m/s': (3.6, _('%.01f km/h')), 'kmh_km/h': (1.0, _('%.01f km/h')), 'kmh_mph': (1.61, _('%.01f km/h')),
			}
			_conv = _windconv.get(windtype + '_' + _windtype)
			if _conv:
				msnweather['Windspeed'] = _conv[1] % (float(_windspeed) * _conv[0])
			else:
				msnweather['Windspeed'] = tree.weather.current.attrib.get('windspeed')
				print("[WeatherMSN] Please fix %s to %s convertion for %s" % (windtype, _windtype, msnweather['Windspeed']))

			msnweather['Date'] = tree.weather.current.attrib['date']
			msnweather['Shortdate'] = tree.weather.current.attrib['shortday']
			msnweather['Day'] = tree.weather.current.attrib['day']
			msnweather['Shortday'] = tree.weather.current.attrib['shortday']

			i = 0
			for forecast in tree.weather.forecast:
				temp = float(forecast[i].attrib['low'])
				msnweather['Lowtemp%s' % i] = '+' + forecast[i].attrib['low'] if temp > 0 else forecast[i].attrib['low']
				temp = float(forecast[i].attrib['high'])
				msnweather['Hightemp%s' % i] = '+' + forecast[i].attrib['high'] if temp > 0 else forecast[i].attrib['high']
				msnweather['Picon%s' % i] = forecast[i].attrib['skycodeday']
				msnweather['Date%s' % i] = forecast[i].attrib['date'] # TODO: format from yyyy-mm-dd to UI date?
				msnweather['Day%s' % i] = forecast[i].attrib['day']
				msnweather['Shortdate%s' % i] = forecast[i].attrib['shortday'] + ' ' + forecast[i].attrib['date'].split('-')[2].strip()
				msnweather['Shortday%s' % i] = forecast[i].attrib['day']
				msnweather['Skytext%s' % i] = forecast[i].attrib['skytextday']
				msnweather['Precip%s' % i] = forecast[i].attrib['precip'] + ' %s' % chr(37)
				msnweather['Temp%s' % i] = "%s%s%s / %s%s%s" % (msnweather['Hightemp%s' % i], chr(176), degreetype, msnweather['Lowtemp%s' % i], chr(176), degreetype)
				i += 1
		except Exception as e:
			print("[TranspBAMSNWeather2] Error during parsing xml: %s" % e)

		if self.type == 'Vfd':
			try:
				weze = msnweather['Skytext'].split(' ')[1]
			except:
				weze = msnweather['Skytext']
			info = msnweather['Temp'] + ' ' + weze
		elif self.type in msnweather:
			info = msnweather[self.type]
		else:
			print("[TranspBAMSNWeather2] requesting unknown type %s" % self.type)

		return info

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))

