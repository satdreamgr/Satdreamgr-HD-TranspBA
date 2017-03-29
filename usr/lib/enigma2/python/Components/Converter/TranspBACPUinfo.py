# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class TranspBACPUinfo(Converter, object):

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
                if os.path.exists('/proc/stb/fp/temp_sensor_avs'):
                        temp = open('/proc/stb/fp/temp_sensor_avs').read().strip()
                if os.path.exists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
                        temp = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()[:2]
                if temp:
                        return _("%s°C") % temp
                return ""

        text = property(getText)


















