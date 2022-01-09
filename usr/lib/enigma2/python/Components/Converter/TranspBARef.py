from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from Components.Element import cached
from NavigationInstance import instance as navInstance


class TranspBARef(Converter, Poll):
    ServiceRef = 0

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        if "ServiceRef" in type:
            self.type = self.ServiceRef

    def refservice(self):
        playref = navInstance.getCurrentlyPlayingServiceReference()
        if playref:
            refstr = playref.toString()
            if "%3a//" in refstr:
                ref = refstr.split(":")
                refservice = ref[10].replace("%3a", ":")
                return refservice
            else:
                return ""

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return ""
        if (self.type == self.ServiceRef):
            return str(self.refservice())

    text = property(getText)
