import sublime
import traceback
import os
import sys
import time
import re
import json

d = os.path.split(__file__)
p = d[0]

f = open(d[0]+'/ftpconfig.json',encoding='utf-8')

config = json.load(f)


st_version = 2
if int(sublime.version()) > 3000:
	st_version = 3

platform = sublime.platform()

reloading = {
	'happening': False,
	'shown': False
}

# sublime.error_message('msg')
# sublime.message_dialog('msg')
# result = sublime.ok_cancel_dialog('msg','ok')

# w = sublime.active_window()
# w.create_output_panel('ftp')
# w.show_input_panel('','welcome',lambda str:sublime.error_message('ok'),lambda str:print(str),lambda:print(11))
# w.show_quick_panel('4554545',lambda chid:sublime.error_message('f')) 

# w = sublime.active_window()
# v = w.active_view()
# v.set_encoding('UTF-8')
# v.encoding() == UTF-8


w = sublime.active_window()
v = w.active_view()

reload_mods = []
for mod in sys.modules:
	if (mod[0:7] == 'FTP.ftp' or mod[0:4] == 'ftp.' or mod == 'ftp') and sys.modules[mod] is not None:
		reload_mods.append(mod)
		reloading['happening'] = True

# Prevent popups during reload, saving the callbacks for re-adding later
if reload_mods:
	old_callbacks = {}
	hook_match = re.search("<class '(\w+).ExcepthookChain'>", str(sys.excepthook))
	if hook_match:
		_temp = __import__(hook_match.group(1), globals(), locals(), ['ExcepthookChain'], -1)
		ExcepthookChain = _temp.ExcepthookChain
		old_callbacks = ExcepthookChain.names
	sys.excepthook = sys.__excepthook__

mods_load_order = [
	'ftp',
	'ftp.commands',
	'ftp.listenrs'
]
# print(reload_mods)
mod_load_prefix = ''
if st_version == 3:
	mod_load_prefix = 'FTP.'
	from imp import reload

for mod in mods_load_order:
	if mod_load_prefix + mod in reload_mods:
		reload(sys.modules[mod_load_prefix + mod])


need_package_control_upgrade = False
try:	
	from .ftp.commands import (
		FtpUploadFileCommand,
		FtpDownloadFileCommand,
		FtpUploadFolderCommand,
		FtpDownloadFolderCommand,
		FtpDiffRemoteFileCommand
	)
	from .ftp.listeners import (
		FtpAutoConnectListener
	)
#failure to load and try again
except(ImportError):
	from .ftp.commands import (
		FtpUploadFileCommand,
		FtpDownloadFileCommand,
		FtpUploadFolderCommand,
		FtpDownloadFolderCommand,
		FtpDiffRemoteFileCommand
	)
	from .ftp.listeners import (
		FtpAutoConnectListener
	)
except(ImportError) as e:
	if str(e).find('bad magic number') != -1:
		need_package_control_upgrade = True
	else:
		raise
