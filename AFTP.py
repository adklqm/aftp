# conding:utf-8
import sublime,sublime_plugin
import os
import re
import sys
import traceback

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
