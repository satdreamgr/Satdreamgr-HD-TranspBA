from os.path import join as pathjoin

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import SCOPE_CURRENT_SKIN, fileExists, resolveFilename
from Tools.LoadPixmap import LoadPixmap


class TranspBAPiconProv(Renderer):

    __module__ = __name__
    searchPaths = (resolveFilename(SCOPE_CURRENT_SKIN), '/media/cf/', '/media/sda1/', '/media/usb/', '/media/hdd/')

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'piconProv'
        self.nameCache = {}
        self.pngname = ''

    def applySkin(self, desktop, parent):
        attribs = []
        for (attrib, value) in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                sname = self.source.text
                sname = sname.upper()
                pngname = self.nameCache.get(sname, '')
                if pngname == '':
                    pngname = self.findPicon(sname)
                    if pngname != '':
                        self.nameCache[sname] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/picon_default.png')
                    self.nameCache['default'] = pngname
            if self.pngname != pngname:
                self.pngname = pngname
                self.runanim()
                self.instance.setPixmapFromFile(self.pngname)

    def findPicon(self, serviceName):
        for path in self.searchPaths:
            pngname = pathjoin(path, self.path, serviceName + '.png')
            if fileExists(pngname):
                return pngname
        return ''

    def runanim(self):
        self.slide = 8
        animok = True
        if animok == True:
            self.pics = []
            for x in range(self.slide):
                self.pics.append(LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, 'spinner/a%d.png' % x)))
            self.timer = eTimer()
            self.timer.callback.append(self.timerEvent)
            self.timer.start(1, True)
        else:
            self.instance.setPixmapFromFile(self.pngname)

    def timerEvent(self):
        if self.slide != 0:
            self.timer.stop()
            self.instance.setPixmap(self.pics[(self.slide - 1)])
            self.slide = (self.slide - 1)
            self.timer.start(1, True)
        else:
            self.timer.stop()
            self.instance.setPixmapFromFile(self.pngname)
