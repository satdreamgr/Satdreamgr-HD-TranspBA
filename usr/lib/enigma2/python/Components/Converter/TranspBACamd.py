from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from Tools.Directories import fileExists


class TranspBACamd(Converter, Poll):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 2000
		self.poll_enabled = True

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		serlist = None
		camdlist = None
		nameemu = []
		nameser = []
		if not info:
			return ""
		if fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				for line in open("/etc/init.d/softcam"):
					if line.find("echo") > -1:
						nameemu.append(line)
				camdlist = "%s" % nameemu[1].split('"')[1]
			except:
				pass
			try:
				for line in open("/etc/init.d/cardserver"):
					if line.find("echo") > -1:
						nameser.append(line)
				serlist = "%s" % nameser[1].split('"')[1]
			except:
				pass
			if serlist is None:
				serlist = ""
			elif camdlist is None:
				camdlist = ""
			elif serlist is None and camdlist is None:
				serlist = ""
				camdlist = ""
			return ("%s %s" % (serlist, camdlist))
		if serlist is not None:
			try:
				cardserver = ""
				for current in serlist.readlines():
					cardserver = current
				serlist.close()
			except:
				pass
		else:
			cardserver = "NA"
		if camdlist is not None:
			try:
				emu = ""
				for current in camdlist.readlines():
					emu = current
				camdlist.close()
			except:
				pass
		else:
			emu = "NA"
		return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
