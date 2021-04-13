from . import _
from Components.ActionMap import ActionMap
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigYesNo, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS
from shutil import move
import os.path


SKIN_NAME = resolveFilename(SCOPE_CURRENT_SKIN, "skin.xml")
WEATHER_PLUGIN = resolveFilename(SCOPE_PLUGINS, 'Extensions/WeatherMSN/plugin.pyo')


config.plugins.SatdreamgrTranspBA = ConfigSubsection()
config.plugins.SatdreamgrTranspBA.SkinColor = ConfigSelection(default="#20000000", choices=[
	("#20000000", _("default")),
	("#00000000", _("black")),
	("#50000000", _("ultra transparent")),
	("#00102030", _("blue")),
	("#00002222", _("green")),
	("#00080022", _("navy blue")),
	("#00333333", _("grey"))
])
config.plugins.SatdreamgrTranspBA.infobarStyle = ConfigSelection(default="full", choices=[
	("simple", _("simple")),
	("full", _("full")),
	("full_bottom", _("full bottom"))
])

config.plugins.SatdreamgrTranspBA.weather = ConfigYesNo(default=False)


class TranspBASkinSetup(ConfigListScreen, Screen):

	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("TranspBA skin setup"))
		self.skinName = ["TranspBASkinSetup", "Setup"]

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["description"] = Label("") # filled automatically when calling createSummary()

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"ok": self.go,
			"green": self.go,
		}, -2)

		configlist = []

		configlist.append(getConfigListEntry(_("Skin color"),
			config.plugins.SatdreamgrTranspBA.SkinColor,
			_("Choose the background color of the skin.")))

		configlist.append(getConfigListEntry(_("Infobar style"),
			config.plugins.SatdreamgrTranspBA.infobarStyle,
			_("Select the type of the infobar.")))

		configlist.append(getConfigListEntry(_("Weather on infobar"),
			config.plugins.SatdreamgrTranspBA.weather,
			_("Show weather information on infobar (the MSN Weather plugin must be installed in your receiver).")))

		ConfigListScreen.__init__(self, configlist, session, self.checkWeatherConfig)

	def go(self):
		if self["config"].isChanged():
			self.restart()
		else: # if no change is made don't re-apply same settings, just close
			self.close()

	def checkWeatherConfig(self):
		weather = config.plugins.SatdreamgrTranspBA.weather
		current = self["config"].getCurrent()[1]
		if current == weather and current.value is True and not os.path.isfile(WEATHER_PLUGIN):
			def installWeatherMsnCb(answer):
				if answer is True:
					self.session.openWithCallback(self.restart, Console, _("Installing WeatherMSN plugin..."), ["opkg install enigma2-plugin-extensions-weathermsn"])
				else:
					current.value = False
			msg = _("The 'WeatherMSN' plugin is required to display weather information. Do you want to install it now?")
			self.session.openWithCallback(installWeatherMsnCb, MessageBox, msg, MessageBox.TYPE_YESNO)
			
	def restart(self):
		msg = _("Your receiver will be restarted in order to apply the new skin settings. Do you want to proceed?")
		self.session.openWithCallback(self.applySettings, MessageBox, msg, MessageBox.TYPE_YESNO, timeout=10)			

	def applySettings(self, answer):
		if answer is True:
			if patchSkin():
				self.saveAll()
				self.session.open(TryQuitMainloop, 3)
			else:
				self.session.open(MessageBox, _("Error applying color settings!"), MessageBox.TYPE_ERROR)


def patchSkin():
	def applyColor(lines):
		updates = []
		for line in lines:
			if "<color name=\"transpBA\" value=\"" in line:
				updates.append("    <color name=\"transpBA\" value=\"%s\" />\n" % config.plugins.SatdreamgrTranspBA.SkinColor.value)
			else:
				updates.append(line)
		return updates

	def applyInfobarStyle(lines):
		value = {
			"simple": "InfoBar_a",
			"full": "InfoBar_b",
			"full_bottom": "InfoBar_c"
		}
		updates = []
		for line in lines:
			if "<panel name=\"InfoBar_" in line:
				updates.append("    <panel name=\"%s\" />\n" % value.get(config.plugins.SatdreamgrTranspBA.infobarStyle.value, "InfoBar_a"))
			else:
				updates.append(line)
		return updates

	def applyInfobarStyle1(lines):
		value = {
			"simple": "SecondInfoBar_a",
			"full": "SecondInfoBar_bc",
			"full_bottom": "SecondInfoBar_bc"		
			}
		updates = []

		for line in lines:

			if "<panel name=\"SecondInfoBar_" in line:
				updates.append("    <panel name=\"%s\" />\n" % value.get(config.plugins.SatdreamgrTranspBA.infobarStyle.value, "SecondInfoBar_bc"))			
			else:
				updates.append(line)
		return updates	

	def applyWeather(lines):
		value = {
			"simple": "WeatherMSN_a",
			"full": "WeatherMSN_b",
			"full_bottom": "WeatherMSN_c"
		}
		updates = []
		for line in lines:
			if "<panel name=\"WeatherMSN_" in line:
				if config.plugins.SatdreamgrTranspBA.weather.value:
					updates.append("    <panel name=\"%s\" />\n" % value.get(config.plugins.SatdreamgrTranspBA.infobarStyle.value, "WeatherMSN_a"))
				else:
					updates.append("    <panel name=\"WeatherMSN_off\" />\n")
			else:
				updates.append(line)
		return updates

	try:
		with open(SKIN_NAME, "r") as fd:
			lines = fd.readlines()
			lines = applyColor(lines)
			lines = applyInfobarStyle(lines)	
			lines = applyInfobarStyle1(lines)
			lines = applyWeather(lines)
			with open(SKIN_NAME, "w") as fd:
				for line in lines:
					fd.writelines(line)
		return True
	except (IOError, OSError):
		pass
	return False


def main(session, **kwargs):
	weather = config.plugins.SatdreamgrTranspBA.weather
	with open(SKIN_NAME, "r") as f:
		if "<panel name=\"WeatherMSN_off\" />" in f.read():
			weather.value = False # for compatibility with existing configs
			weather.save()
	if weather.value is True and not os.path.isfile(WEATHER_PLUGIN):
		def confirmedCb(answer):
			if answer is True:
				weather.value = False
				session.open(TranspBASkinSetup)
		msg = _("The 'WeatherMSN' plugin was not found. Weather on infobar has been turned off.")
		session.openWithCallback(confirmedCb, MessageBox, msg, MessageBox.TYPE_INFO, timeout=5)
	else:
		session.open(TranspBASkinSetup)


def menu(menuid, **kwargs):
	if menuid == "gui" and config.skin.primary_skin.value == "Satdreamgr-HD-TranspBA/skin.xml":
		return [(_("TranspBA skin setup"), main, "transpba_skin_setup", None)]
	return []


def autostart(reason, **kwargs):
	if reason == 0 and config.skin.primary_skin.value == "Satdreamgr-HD-TranspBA/skin.xml":
		if not patchSkin():
			print "[TranspBASkinSetup] Error: Unable to update skin!"


def Plugins(**kwargs):
	return [
		PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart),
		PluginDescriptor(name=_("TranspBA skin setup"), description=_("Setup tool for Satdreamgr-HD-TranspBA skin"), where=[PluginDescriptor.WHERE_MENU], fnc=menu)
	]
