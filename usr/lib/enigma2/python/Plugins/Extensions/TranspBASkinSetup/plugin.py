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
from Tools.Directories import fileExists, resolveFilename, SCOPE_CONFIG, SCOPE_PLUGINS
from shutil import move
import os.path


SKIN_NAME = resolveFilename(SCOPE_CONFIG, "skin_user_Satdreamgr-HD-TranspBA.xml")
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
config.plugins.SatdreamgrTranspBA.infobarStyle = ConfigSelection(default="simple", choices=[
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
			"red":self.keyCancel,
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
			msg = _("Your receiver will be restarted in order to apply the new skin settings. Do you want to proceed?")
			self.session.openWithCallback(self.applySettings, MessageBox, msg, MessageBox.TYPE_YESNO)
		else: # if no change is made don't re-apply same settings, just close
			self.close()

	def checkWeatherConfig(self):
		weather = config.plugins.SatdreamgrTranspBA.weather
		current = self["config"].getCurrent()[1]
		if current == weather and current.value is True and not os.path.isfile(WEATHER_PLUGIN):
			def installWeatherMsnCb(answer):
				if answer is True:
					self.session.open(Console, _("Installing WeatherMSN plugin..."), ["opkg install enigma2-plugin-extensions-weathermsn"], showStartStopText=False)
					self.applyColor()
					self.applyInfobarStyle()
					self.applyWeather()
					self.saveAll()
					self.session.open(TryQuitMainloop, 3)
				else:
					current.value = False
			msg = _("The 'WeatherMSN' plugin is required to display weather information. Do you want to install it now?")
			self.session.openWithCallback(installWeatherMsnCb, MessageBox, msg, MessageBox.TYPE_YESNO)

	def applySettings(self, answer):
		if answer is True:
			self.applyColor()
			self.applyInfobarStyle()
			self.applyWeather()
			self.saveAll()
			self.session.open(TryQuitMainloop, 3)

	def applyColor(self):
		skinSearchAndReplace = []
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#20000000":
			skinSearchAndReplace.append(["#20000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00000000":
			skinSearchAndReplace.append(["#00000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#50000000":
			skinSearchAndReplace.append(["#50000000", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00102030":
			skinSearchAndReplace.append(["#00102030", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00002222":
			skinSearchAndReplace.append(["#00002222", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00080022":
			skinSearchAndReplace.append(["#00080022", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		if config.plugins.SatdreamgrTranspBA.SkinColor.value != "#00333333":
			skinSearchAndReplace.append(["#00333333", config.plugins.SatdreamgrTranspBA.SkinColor.value])
		try:
			f = open(SKIN_NAME, "r")
			lines = f.readlines()
			f.close()
			pimpedLines = []
			for line in lines:
				for item in skinSearchAndReplace:
					line = line.replace(item[0], item[1])
				pimpedLines.append(line)
			f = open(SKIN_NAME, "w")
			for line in pimpedLines:
				f.writelines(line)
			f.close()
		except:
			self.session.open(MessageBox, _("Error applying color settings!"), MessageBox.TYPE_ERROR)

	def applyInfobarStyle(self):
		f = open(SKIN_NAME, "r")
		chaine = f.read()
		f.close()
		infobarStyle = config.plugins.SatdreamgrTranspBA.infobarStyle.value
		if infobarStyle == "simple":
			result = chaine.replace("infobar_b.xml", "infobar_a.xml").replace("infobar_c.xml", "infobar_a.xml")
		elif infobarStyle == "full":
			result = chaine.replace("infobar_a.xml", "infobar_b.xml").replace("infobar_c.xml", "infobar_b.xml")
		elif infobarStyle == "full_bottom":
			result = chaine.replace("infobar_a.xml", "infobar_c.xml").replace("infobar_b.xml", "infobar_c.xml")
		f = open(SKIN_NAME, "w")
		f.write(result)
		f.close()

	def applyWeather(self):
		f = open(SKIN_NAME, "r")
		chaine = f.read()
		f.close()
		weather = config.plugins.SatdreamgrTranspBA.weather.value
		infobarStyle = config.plugins.SatdreamgrTranspBA.infobarStyle.value
		if "weather" in chaine:
			if weather is True:
				if infobarStyle == "simple" or infobarStyle == "full_bottom":
					result = chaine.replace("weather_off.xml", "weather_ac.xml").replace("weather_b.xml", "weather_ac.xml")
				elif infobarStyle == "full":
					result = chaine.replace("weather_off.xml", "weather_b.xml").replace("weather_ac.xml", "weather_b.xml")
			else:
				result = chaine.replace("weather_ac.xml", "weather_off.xml").replace("weather_b.xml", "weather_off.xml")
		else:
			if weather is True:
				if infobarStyle == "simple" or infobarStyle == "full_bottom":
					result = chaine.replace('<skin>\n', '<skin>\n  <include filename="weather_ac.xml" />\n')
				elif infobarStyle == "full":
					result = chaine.replace('<skin>\n', '<skin>\n  <include filename="weather_b.xml" />\n')
			else:
				result = chaine.replace('<skin>\n', '<skin>\n  <include filename="weather_off.xml" />\n')
		f = open(SKIN_NAME, "w")
		f.write(result)
		f.close()


def main(session, **kwargs):
	weather = config.plugins.SatdreamgrTranspBA.weather
	with open(SKIN_NAME, "r") as f:
		if "weather" not in f.read():
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


def Plugins(**kwargs):
	return PluginDescriptor(
		name=_("TranspBA skin setup"),
		description=_("Setup tool for Satdreamgr-HD-TranspBA skin"),
		where=PluginDescriptor.WHERE_MENU,
		fnc=menu)
