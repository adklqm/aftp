#conding:utf-8

import sublime,sublime_plugin,json
from   .commands import getConfig,getLocalPath

class AftpAutoConnectListener(sublime_plugin.EventListener):

    #Called just before a view is saved.
    def on_pre_save(self,edit):
        pass

    #Called just after a view is saved.
    def on_post_save(self,edit):
        active_window = sublime.active_window()
        path = active_window.active_view().file_name()

        localDir = getLocalPath(path)
        config   = getConfig(localDir)
        try:
            upload_on_save = config['upload_on_save']
            if False == upload_on_save:
                return
        except Exception:
            return
        active_window.run_command('aftp_upload_file',{"paths":[]})
