from Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iAudioTrackInfo
from Components.config import config
from Components.Element import cached

class TranspBAAudioTrack(Poll, Converter, object):
	atype = 0
	vtype = 1
	avtype = 2

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if  type == "atype":
			self.type = self.atype
		elif  type == "vtype":
			self.type = self.vtype
		elif  type == "avtype":
			self.type = self.avtype

	@cached
	def getText(self):
		self.stream = { 'atype':"", 'vtype':"", 'avtype':"",}
		streaminfo = ""
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		audio = service.audioTracks()
		if audio:
			if audio.getCurrentTrack() > -1:
				self.stream['atype'] = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()).replace(",","")
		self.stream['vtype'] = ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "HEVC", "H265", "AVS", "N/A")[info.getInfo(iServiceInformation.sVideoType)]
		self.stream['avtype'] = ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "HEVC", "H265", "AVS", "N/A")[info.getInfo(iServiceInformation.sVideoType)] + "\c00?25=41" + " / " + "\c0078:0=7" + self.stream['atype']

		if self.type == self.atype:
			streaminfo = self.stream['atype']
		elif self.type == self.vtype:
			streaminfo = self.stream['vtype']
		elif self.type == self.avtype:
			streaminfo = self.stream['avtype']
		return streaminfo

	text = property(getText)
