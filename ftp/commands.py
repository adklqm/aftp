#conding:utf-8

import  sublime,sublime_plugin
import  os
from    .filetransfer import FileTransfer as Ftp
import  json
import  ftplib
import  re

#Instance of Ftp
FTP         = False
#It is a path for ftp-config.json
CONFIG_PATH = False

def getFtp(path):
    global FTP
    global CONFIG_PATH

    tmp = getConfigPath(path)
    if False == tmp:
        CONFIG_PATH = False
        if False != FTP:
            FTP.close()
            FTP = False
            return

    if tmp != CONFIG_PATH:
        CONFIG_PATH = tmp
        if FTP != False:
            FTP.close()
            FTP = False

    if False == FTP:
        config = getConfig()
        if len(config) < 1:
            return
        FTP = Ftp(config['host'])
        try:
            FTP.Login(config['user'],config['password'])
        except(ftplib.error_perm):
            FTP = False


def getConfig():
    global CONFIG_PATH
    if False == CONFIG_PATH:
        return []
    fp     = open( os.path.join(CONFIG_PATH,'ftp-config.json') ,encoding = 'utf-8')
    config = json.load(fp)
    return config


def getConfigPath(path):
    fileDir = (os.path.split(path))[0]
    tmp     = ''
    for x in os.listdir(fileDir):
        tmp = os.path.join(fileDir,x)
        if( os.path.isfile(tmp) and "ftp-config.json" == x ):
            return fileDir
    if(len(fileDir) < 4):
        return False
    return getConfigPath(fileDir)


def getRemotePath(path):
    global CONFIG_PATH
    getConfigPath(path)
    config = getConfig()
    if len(config) < 1:
        return
    remotePath = config['remote_path']
    #If it doesn't end with "/"
    if remotePath[-1] != "/":
        remotePath = remotePath + "/"

    tmp = path.replace(CONFIG_PATH + "\\",'')
    tmp = tmp.replace("\\","/")
    remotePath = remotePath + tmp
    print(remotePath)
    return remotePath


def valid(**args):
    print(args)
    return True
    if('file' == args['type']):
        if len(args) < 2:
            return True
        else:
            if os.path.isdir(args['paths'][0]):
                return False
            else:
                return True
    else:
        if len(args) < 2:
            return False
        else:
            if os.path.isdir(args['paths'][0]):
                return True
            else:
                return False

class FtpUploadFileCommand(sublime_plugin.TextCommand):

    def run(self,edit,**args):
        viewPath = self.view.file_name()
        getFtp(viewPath)
        global FTP
        if(FTP == False):
            return

        path = self.view.file_name()
        FTP.UpLoadFile(path,getRemotePath(path))

    #命令是否可用
    def is_enabled(self,**args):

        viewPath = self.view.file_name()
        args['type'] = 'file'
        return valid(**args)

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'file'
        return valid(**args)

    #是否允许接收事件（鼠标）参数
    def want_event(self):
        return False

class FtpDownloadFileCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        viewPath = self.view.file_name()
        getFtp(viewPath)
        global FTP
        if(FTP == False):
            return

        path = self.view.file_name()
        FTP.DownLoadFile(path,getRemotePath(path))

    #命令是否可用
    def is_enabled(self,**args):
        args['type'] = 'file'
        return valid(sdfsf='sfsfs')

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'file'
        return valid(**args)

class FtpUploadFolderCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        path = args['paths'][0]
        getFtp(path)
        global FTP
        if(FTP == False):
            return

        FTP.UpLoadFolder(path,getRemotePath(path))


    #命令是否可用
    def is_enabled(self,**args):

        args['type'] = 'folder'
        return valid(paths=args['paths'],type='dddfff')

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'folder'
        return valid(**args)


class FtpDownloadFolderCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        path = args['paths'][0]
        getFtp(path)
        global FTP
        if(False == FTP):
            return

        FTP.DownLoadFolder(path,getRemotePath(path))

    #命令是否可用
    def is_enabled(self,**args):
        args['type'] = 'folder'
        return valid(**args)

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'folder'
        return valid(**args)


class FtpDiffRemoteFileCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        print(111)
        print(self.view.file_name())

    #命令是否可用
    def is_enabled(self,**args):
        args['type'] = 'file'
        return valid(**args)

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'file'
        return valid(**args)


#Generate a config file for ftp connect
class FtpMapToRemotePathCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        print(1)

    #命令是否可用
    def is_enabled(self,**args):
        args['type'] = 'file'
        return True

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'file'
        return True


#Generate a config file for ftp connect
class FtpMapToRemoteFileCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        print(1)

    #命令是否可用
    def is_enabled(self,**args):
        args['type'] = 'file'
        return True

    #命令是否可见
    def is_visible(self,**args):
        args['type'] = 'file'
        return True
