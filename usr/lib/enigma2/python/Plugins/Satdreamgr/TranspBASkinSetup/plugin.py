from . import _
from Components.ActionMap import ActionMap
from Components.config import config, configfile, ConfigSubsection, ConfigSelection, ConfigYesNo, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import SCOPE_CURRENT_SKIN, SCOPE_CONFIG, fileExists, resolveFilename
from shutil import move
import os


SKIN_NAME = "Satdreamgr-HD-TranspBA"


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

		ConfigListScreen.__init__(self, configlist, session)

	def go(self):
		if self["config"].isChanged():
			msg = _("Your receiver will be restarted in order to apply the new skin settings. Do you want to proceed?")
			self.session.openWithCallback(self.applySettings, MessageBox, msg, MessageBox.TYPE_YESNO)
		else: # if no change is made don't re-apply same settings, just close
			self.close()

	def applySettings(self, answer):
		if answer is True:
			self.applyColor()
			self.applyInfobarStyle()
			self.applyWeather()
			self.saveAll()
			self.session.open(TryQuitMainloop, 3)

	def applyColor(self):
		filename = resolveFilename(SCOPE_CONFIG, "skin_user_%s.xml" % SKIN_NAME)

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
			f = open(filename, "r")
			lines = f.readlines()
			f.close()

			pimpedLines = []
			for line in lines:
				for item in skinSearchAndReplace:
					line = line.replace(item[0], item[1])
				pimpedLines.append(line)

			f = open(filename, "w")
			for line in pimpedLines:
				f.writelines(line)
			f.close()
		except:
			self.session.open(MessageBox, _("Error applying color settings!"), MessageBox.TYPE_ERROR)

	def applyInfobarStyle(self):
		filename = resolveFilename(SCOPE_CONFIG, "skin_user_%s.xml" % SKIN_NAME)
		f = open(filename, "r")
		chaine = f.read()
		f.close()
		infobarStyle = config.plugins.SatdreamgrTranspBA.infobarStyle.value
		if infobarStyle == "simple":
			result = chaine.replace("infobar_b.xml", "infobar_a.xml").replace("infobar_c.xml", "infobar_a.xml")
		elif infobarStyle == "full":
			result = chaine.replace("infobar_a.xml", "infobar_b.xml").replace("infobar_c.xml", "infobar_b.xml")
		elif infobarStyle == "full_bottom":
			result = chaine.replace("infobar_a.xml", "infobar_c.xml").replace("infobar_b.xml", "infobar_c.xml")
		f = open(filename, "w")
		f.write(result)
		f.close()

	def applyWeather(self):
		weather = config.plugins.SatdreamgrTranspBA.weather.value
		for i in ("a", "b", "c"): # infobar names
			if weather is True:
				self.writeWeather(True, i)
			else:
				self.writeWeather(False, i)

	def writeWeather(self, enable, infobar): # Weather settings are lost between skin updates - We should refactor the skin code
		filename = resolveFilename(SCOPE_CURRENT_SKIN, "infobar_%s.xml" % infobar)
		f = open(filename, "r")
		chaine = f.read()
		f.close()
		if enable is True:
			result = chaine.replace("<!--<eLabel />", "<ePixmap />")
		else:
			result = chaine.replace("<ePixmap />", "<!--<eLabel />")
		f = open(filename, "w")
		f.write(result)
		f.close()


def main(session, **kwargs):
		session.open(TranspBASkinSetup)


def menu(menuid, **kwargs):
	if menuid == "gui" and config.skin.primary_skin.value == "%s/skin.xml" % SKIN_NAME:
		return [(_("TranspBA skin setup"), main, "transpba_skin_setup", None)]
	return []


def Plugins(**kwargs):
	return PluginDescriptor(
		name=_("TranspBA skin setup"),
		description=_("Setup tool for Satdreamgr-HD-TranspBA skin"),
		where=PluginDescriptor.WHERE_MENU,
		fnc=menu)
