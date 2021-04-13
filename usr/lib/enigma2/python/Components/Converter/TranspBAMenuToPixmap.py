# -*- coding: UTF-8 -*-
#
# Converter - TranspBAMenuToPixmap
# Developer - SatDreamGr
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import SCOPE_CURRENT_SKIN, resolveFilename
from Tools.LoadPixmap import LoadPixmap

MENUS = {
	# Menu
	'softcam_setup': 'menu/panel/softcam.png',
	'auto_cam_setup': 'menu/setup/assign.png',
	# menu_mainmenu
	'panel_setup': 'menu/panel.png',
	'media_player': 'menu/media-player.png',
	'timer_edit': 'menu/timer.png',
	'info_screen': 'menu/information.png',
	'plugin_selection': 'menu/plugins.png',
	'standby_restart_list': 'menu/standby.png',
	'setup_selection': 'menu/setup.png',
	'newmenu': 'menu/newmenu.png',
	'youtube_tv': 'menu/youtube.png',
	# menu_information
	'service_info_screen': 'menu/information/service.png',
	'about_screen': 'menu/information/about.png',
	'streaming_clients_info_screen': 'menu/information/streaming.png',
	# menu_setup
	'system_selection': 'menu/setup/system.png',
	'service_searching_selection': 'menu/setup/searching.png',
	'cam_setup': 'menu/setup/common-interface.png',
	'autobackup': 'menu/setup/autobackup.png',
	'ci_setup': 'menu/setup/common-interface.png',
	'ci_assign': 'menu/setup/assign.png',
	'parental_setup': 'menu/setup/parental.png',
	'factory_reset': 'menu/setup/factory.png',
	'software_manager': 'menu/setup/software.png',
	'flash_image': 'menu/setup/flash.png',
	# menu_system
	'device_manager': 'menu/system/devices.png',
	'video_selection': 'menu/system/browser.png',
	'usage_setup': 'menu/system/customize.png',
	'gui_settings': 'menu/information/about.png',
	'expert_selection': 'menu/system/user-interface.png',
	'system_time_setup': 'menu/system/time.png',
	'epg_settings': 'menu/system/epg-settings.png',
	'epg_menu': 'menu/system/epg-menu.png',
	'iptv_config': 'menu/system/iplayer.png',
	'AutomaticCleanup': 'menu/system/broom.png',
	# menu_gui
	'language_setup': 'menu/system/language.png',
	'timezone_setup': 'menu/system/timezone.png',
	'user_interface': 'menu/system/user-interface.png',
	'skin_selector': 'menu/system/skin.png',
	'primary_skin_selector': 'menu/system/skin.png',
	'display_skin_selector': 'menu/system/displayskin.png',
	# menu_video
	'hdmi_cec_setup': 'menu/system/hdmi.png',
	'auto_3d_setup': 'menu/system/osd.png',
	'video_finetune': 'menu/system/video-tuning.png',
	'av_setup': 'menu/system/av-setup.png',
	'subtitle_setup': 'menu/system/subtitles.png',
	'autolanguage_setup': 'menu/system/language.png',
	'sd_position_setup': 'menu/system/av-setup.png',
	'autores_setup': 'menu/system/av-setup.png',
	# menu_expert
	'accesslevel_setup': 'menu/setup.png',
	'recording_setup': 'menu/system/record.png',
	'hardisk_selection': 'menu/system/harddisk.png',
	'network_setup': 'menu/system/network.png',
	'input_device_setup': 'menu/system/input-device.png',
	'lcd_setup': 'menu/system/display.png',
	'keyboard_setup': 'menu/system/keyboard.png',
	'RecordPaths': 'menu/system/recordings-paths.png',
	'hotkey_setup': 'menu/system/hotkey.png',
	'transcoding_setup': 'menu/system/transcoding.png',
	'vfd_ini': 'iconssc/led-display.png',
	# menu_harddisk
	'harddisk_setup': 'menu/system/harddisk-setup.png',
	'harddisk_init': 'menu/system/format.png',
	'harddisk_check': 'menu/system/check-harddisk.png',
	'harddisk_convert': 'menu/system/convert-harddisk.png',
	# menu_scan
	'tuner_setup': 'menu/menu-scan/tuner.png',
	'auto_scan': 'menu/menu-scan/auto.png',
	'manual_scan': 'menu/menu-scan/manual.png',
	'satfinder': 'menu/menu-scan/satfinder.png',
	'blindscan': 'menu/menu-scan/blindscan.png',
	'positioner_setup': 'menu/menu-scan/positionner.png',
	'fastscan': 'menu/menu-scan/fast.png',
	'cablescan': 'menu/menu-scan/cable.png',
	'fallbacktuner_settings': 'menu/menu-scan/fallback.png',
	 # menu_shutdown
	'sleep': 'menu/standby/timer.png',
	'standby': 'menu/standby/standby.png',
	'restart': 'menu/standby/restart.png',
	'restart_enigma': 'menu/standby/restart-enigma.png',
	'deep_standby': 'menu/standby/off.png',
	'multiboot': 'menu/standby/multiboot.png',
	'restart_enigma_debug': 'menu/standby/debug.png',
}


class TranspBAMenuToPixmap(Converter):

	def __init__(self, type):
		Converter.__init__(self, type)

	def selChanged(self):
		self.downstream_elements.changed((self.CHANGED_ALL, 0))

	@cached
	def getPixmap(self):
		cur = self.source.current
		if cur and len(cur) > 2 and cur[2]:
			return LoadPixmap(resolveFilename(SCOPE_CURRENT_SKIN, MENUS.get(cur[2], 'menu/default.png')))
		return None

	pixmap = property(getPixmap)

	def changed(self, what):
		if what[0] == self.CHANGED_DEFAULT:
			self.source.onSelectionChanged.append(self.selChanged)
		Converter.changed(self, what)
