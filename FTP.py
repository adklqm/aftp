# conding:utf-8
import sublime,sublime_plugin
import traceback
import os
import sys
import time
import re
import json
import  ftplib

# Get path of current dir. d[0] is a directory and d[1] is a file name
dir_arr = os.path.split(__file__)
# Get default config
DEFAULT_CONFIG_PATH = os.path.join(dir_arr[0] + '/default-ftp-config.json')

fp = open(DEFAULT_CONFIG_PATH,encoding = 'utf-8')
DEFAULT_CONFIG = json.load(fp)
fp.close()

# Controls command logging. If enabled, all commands run from key bindings and the menu will 
# Be logged to the console.
# sublime.log_commands(False)

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

# Get refer for active_window
w = sublime.active_window()


panel = w.create_output_panel("ftp")


class SeajsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print(edit.edit_token)
        self.view.insert(edit,1,"ssdfsdf")

w.run_command('show_panel',{"panel":"console"})


# ftp  = ftplib.FTP()
# ftp.set_debuglevel(2)
# ftp.set_pasv(False)
# ftp.connect( '10.0.11.86', 21 )
# ftp.login( 'tccms_dev', 'XFVLj6D4hntswH' )
# fp = open( 'E:\\tccms\\console\\log.text', 'wb' )

# try:
#     ftp.retrbinary( "RETR %s" % ( 'log.text' ), fp.write )
# except:
#     print(55)
#     ftp.set_pasv(True)
#     ftp.retrbinary( "RETR %s" % ( 'log.text' ), fp.write )



# fp.close()
# ftp.close()


# panel.run_command('seajs')
# print(panel.buffer_id())
# panel.is_read_only()
# w.run_command('show_panel',{"panel":"output.ftp"})
# w.run_command('hide_panel',{"panel":"output.sftp"})


# print(w.active_view().encoding())
# print(w.active_view().set_encoding('UTF-8'))

# w.create_output_panel('sftp')



# sublime.run_command("show_panel",{"panel":"output.sftp"})
sublime.run_command("show_panel",{"panel":"console"})
# Show input panel
# w.show_input_panel('','welcome',lambda str:sublime.error_message('ok'),lambda str:print(str),lambda:print(11))

# Show a panel with quick choose
# w.show_quick_panel('4554545',lambda chid:sublime.error_message('f')) 

# w = sublime.active_window()
# v = w.active_view()
# v.set_encoding('UTF-8')`
# v.encoding() == UTF-8


# w = sublime.active_window()
# v = w.active_view()

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

mod_load_prefix = ''
if 3 == st_version:
    mod_load_prefix = 'FTP.'
    from imp import reload

for mod in mods_load_order:
    if mod_load_prefix + mod in reload_mods:
        reload(sys.modules[mod_load_prefix + mod])

# Check whether the plugin need to be upgraded
need_package_control_upgrade = False

# Load dependency
try:
    from .ftp.commands import (
        FtpUploadFileCommand,
        FtpDownloadFileCommand,
        FtpUploadFolderCommand,
        FtpDownloadFolderCommand,
        FtpDiffRemoteFileCommand,
        FtpMapToRemoteCommand
    )
    from .ftp.listeners import (
        FtpAutoConnectListener
    )
# If failure to load with try again
except(ImportError):
    from .ftp.commands import (
        FtpUploadFileCommand,
        FtpDownloadFileCommand,
        FtpUploadFolderCommand,
        FtpDownloadFolderCommand,
        FtpDiffRemoteFileCommand,
        FtpMapToRemoteCommand
    )
    from .ftp.listeners import (
        FtpAutoConnectListener
    )
# Throw error
except(ImportError) as e:
    if -1 != str(e).find('bad magic number'):
        need_package_control_upgrade = True
    else:
        raise
