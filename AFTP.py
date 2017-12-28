# conding:utf-8
import sublime,sublime_plugin
import os
import re
import sys
import json
import traceback

# Get path of current dir. d[0] is a directory and d[1] is a file name
dir_arr = os.path.split(__file__)
# Get default config
DEFAULT_CONFIG_PATH = os.path.join(dir_arr[0] + '/default-ftp-config.json')
fp                  = open(DEFAULT_CONFIG_PATH,encoding = 'utf-8')
DEFAULT_CONFIG      = json.load(fp)
fp.close()

# Get refer for active_window
ACTIVE_WINDOW = sublime.active_window()
LOG_PANEL     = ACTIVE_WINDOW.create_output_panel("aftp")

# Set sublime text version
st_version = 2
if int(sublime.version()) > 3000:
    st_version = 3

# Returns the platform, which may be "osx", "linux" or "windows"
platform = sublime.platform()

reloading = {
    'happening': False,
    'shown': False
}

# Alert error msg
# sublime.error_message('msg')

# Alert msg
# sublime.message_dialog('msg')

# Show a dialog with confirm and cancel
# result = sublime.ok_cancel_dialog('msg','ok')

# Show input panel
# w.show_input_panel('','welcome',lambda str:sublime.error_message('ok'),lambda str:print(str),lambda:print(11))

# Show a panel with quick choose
# w.show_quick_panel('4554545',lambda chid:sublime.error_message('f'))

# Set view's encode
# view.set_encoding('UTF-8')`
# view.encoding() == UTF-8

reload_mods = []
for mod in sys.modules:
    if (mod[0:7] == 'AFTP.aftp' or mod[0:4] == 'aftp.' or mod == 'aftp') and sys.modules[mod] is not None:
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
    'aftp',
    'aftp.commands',
    'aftp.listenrs'
]

mod_load_prefix = ''
if 3 == st_version:
    mod_load_prefix = 'AFTP.'
    from imp import reload

for mod in mods_load_order:
    if mod_load_prefix + mod in reload_mods:
        reload(sys.modules[mod_load_prefix + mod])

# Check whether the plugin need to be upgraded
need_package_control_upgrade = False

# Load dependency
try:
    from .aftp.commands import (
        AftpUploadFileCommand,
        AftpDownloadFileCommand,
        AftpUploadFolderCommand,
        AftpDownloadFolderCommand,
        AftpDiffRemoteFileCommand,
        AftpMapToRemoteCommand,
        AftpDeleteRemoteFileCommand,
        AftpDeleteRemoteFolderCommand
    )
    from .aftp.listeners import (
        AftpAutoConnectListener
    )
# If failure to load with try again
except(ImportError):
    from .aftp.commands import (
        AftpUploadFileCommand,
        AftpDownloadFileCommand,
        AftpUploadFolderCommand,
        AftpDownloadFolderCommand,
        AftpDiffRemoteFileCommand,
        AftpMapToRemoteCommand,
        AftpDeleteRemoteFileCommand,
        AftpDeleteRemoteFolderCommand
    )
    from .aftp.listeners import (
        AftpAutoConnectListener
    )
# Throw error
except(ImportError) as e:
    if -1 != str(e).find('bad magic number'):
        need_package_control_upgrade = True
    else:
        raise
