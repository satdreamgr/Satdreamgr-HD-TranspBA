from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
import os

class TranspBACamd(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        camd = ''
        camdlist = None
        serlist = None
        if not info:
            return ''
        if fileExists('/etc/init.d/softcam') or fileExists('/etc/init.d/cardserver'):
            try:
                camdlist = os.popen('/etc/init.d/softcam info')
            except:
                pass

            try:
                serlist = os.popen('/etc/init.d/cardserver info')
            except:
                pass

        else:
            return
        if serlist is not None:
            try:
                cardserver = ''
                for current in serlist.readlines():
                    cardserver = current

                serlist.close()
            except:
                pass

        else:
            cardserver = 'NA'
        if camdlist is not None:
            try:
                emu = ''
                for current in camdlist.readlines():
                    emu = current

                camdlist.close()
            except:
                pass

        else:
            emu = 'NA'
        return '%s %s' % (cardserver.split('\n')[0], emu.split('\n')[0])

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, what)
