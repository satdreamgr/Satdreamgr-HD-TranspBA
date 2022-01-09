from Components.Converter.Converter import Converter
from Components.Converter.PliExtraInfo import codec_data
from Components.Converter.Poll import Poll
from Components.Element import cached
from enigma import iServiceInformation


class TranspBAAudioTrack(Poll, Converter, object):
	atype = 0
	vtype = 1
	avtype = 2

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "atype":
			self.type = self.atype
		elif type == "vtype":
			self.type = self.vtype
		elif type == "avtype":
			self.type = self.avtype

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""

		atype = ""
		audio = service.audioTracks()
		if audio and audio.getCurrentTrack() > -1:
			atype = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()).replace(",", "")

		if self.type == self.atype:
			return atype

		vtype = codec_data.get(info.getInfo(iServiceInformation.sVideoType), "N/A")

		if self.type == self.vtype:
			return vtype

		if self.type == self.avtype:
			return vtype + "\c00?25=41" + " / " + "\c0078:0=7" + atype

		return ""

	text = property(getText)
