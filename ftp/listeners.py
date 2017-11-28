#conding:utf-8

import sublime,sublime_plugin

class FtpAutoConnectListener(sublime_plugin.EventListener):

	#Called just before a view is saved.
	def on_pre_save(self,edit):
		w = sublime.active_window()


	#Called just after a view is saved.
	def on_post_save(self,edit):
		pass

