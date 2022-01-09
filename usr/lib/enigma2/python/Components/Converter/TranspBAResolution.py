from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from enigma import iServiceInformation


class TranspBAResolution(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 1000
		self.poll_enabled = True

	def createResolution(self, info):
		xres = info.getInfo(iServiceInformation.sVideoWidth)
		if xres == -1:
			return ""
		yres = info.getInfo(iServiceInformation.sVideoHeight)
		mode = ("i", "p", "", " ")[info.getInfo(iServiceInformation.sProgressive)]
		fps = str((info.getInfo(iServiceInformation.sFrameRate) + 500) // 1000)
		if int(fps) <= 0:
			fps = ""
		return str(xres) + "x" + str(yres) + mode + fps

	@cached
	def getText(self):
		service = self.source.service
		if service is None:
			return ""
		info = service and service.info()

		if not info:
			return ""

		if self.type == "ResolutionString":
			return self.createResolution(info)

	text = property(getText)
