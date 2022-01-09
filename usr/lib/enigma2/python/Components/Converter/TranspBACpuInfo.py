from os.path import exists, isfile
from re import search

from Components.Converter.Converter import Converter
from Components.Element import cached


class TranspBACpuInfo(Converter):

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		if self.type == "CPUtemp":
			try:
				return self.getCPUtemp()
			except:
				pass
		return ""

	def getCPUtemp(self):
		temp = ""
		if exists('/proc/stb/fp/temp_sensor_avs'):
			temp = open('/proc/stb/fp/temp_sensor_avs').read().strip()
		if exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
			temp = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()[:2]
		if isfile("/proc/hisi/msp/pm_cpu"):
			temp = search('temperature = (\d+) degree', open("/proc/hisi/msp/pm_cpu").read()).group(1)
		if temp:
			return "%s°C" % temp
		return ""

	text = property(getText)
