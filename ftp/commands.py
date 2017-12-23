#conding:utf-8
import  sublime,sublime_plugin
import  os
from    .filetransfer import FileTransfer as Ftp
import  json
import  ftplib
import  re
from  ..FTP import DEFAULT_CONFIG,DEFAULT_CONFIG_PATH

#Instance of Ftp
FTP         = False
#It is a path for ftp-config.json
LOCAL_PATH = False
# A json object for FTP
FTP_CONFIG = False

def getFtp(path):
    global FTP
    global LOCAL_PATH
    global FTP_CONFIG

    tmp = getLocalPath(path)
    if False == tmp:
        LOCAL_PATH  = False
        FTP_CONFIG  = False
        if False != FTP:
            FTP.close()
            FTP = False
        print('Load configuration file failed')
        return

    if tmp != LOCAL_PATH:
        LOCAL_PATH = tmp
        FTP_CONFIG = False
        if False != FTP:
            FTP.close()
            FTP = False

    config = getConfig()
    if False == config:
        LOCAL_PATH = False
        FTP_CONFIG = False
        if False != FTP:
            FTP.close()
            FTP = False
        print('Load configuration file failed')
        return

    if False == FTP_CONFIG:
        FTP_CONFIG = config
    elif (config == FTP_CONFIG):
        pass
    else:
        FTP_CONFIG = config
        if False != FTP:
            FTP.close()
            FTP = False

    # Check FTP isn't valid
    if False != FTP:
        if True == FTP.checkConnect():
            pass
        else:
            print('connect is disable')
            FTP = False
    if False == FTP:
        try:
            FTP = Ftp(config)
        except(ftplib.error_perm):
            FTP = False
            print('Connection '+ config['host'] +' failure')
        try:
            FTP.Login()
        except(ftplib.error_perm):
            FTP = False
            print('Login failure as ' + config['user'])




def getConfig():
    global LOCAL_PATH
    if False == LOCAL_PATH:
        return False
        
    fp     = open( os.path.join(LOCAL_PATH,'ftp-config.json') ,encoding = 'utf-8')
    config = json.load(fp)
    return config


def getLocalPath(path):
    fileDir = (os.path.split(path))[0]
    tmp     = ''

    for x in os.listdir(fileDir):
        tmp = os.path.join(fileDir,x)
        if( os.path.isfile(tmp) and "ftp-config.json" == x ):
            return fileDir

    if(len(fileDir) < 4):
        return False
    return getLocalPath(fileDir)


def getRemotePath(path):
    global LOCAL_PATH
    if False == LOCAL_PATH:
        return False

    config = getConfig()
    if False == config:
        return False

    remotePath = config['remote_path']
    #If it doesn't end with "/"
    if remotePath[-1] != "/":
        remotePath = remotePath + "/"

    tmp = path.replace(LOCAL_PATH + "\\",'')
    tmp = tmp.replace("\\","/")
    remotePath  = remotePath + tmp
    return remotePath


def valid(**args):
    config_path = getLocalPath(args['path'])
    if False == config_path:
        if 'transfer' == args['action']:
            return False
        elif 'config' == args['action']:
            if os.path.isdir(args['path']):
                if os.path.isfile( os.path.join(args['path'],'ftp-config.json') ):
                    return False
            return True
        else:
            return False

    else:
        if 'config' == args['action']:
            return False
        else:
            pass

    if 'transfer' == args['action']:
        if 'file' == args['command_type']:
            if os.path.isdir(args['path']):
                return False
            else:
                return True
        elif 'folder' == args['command_type']:
            if os.path.isdir(args['path']):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class FtpUploadFileCommand(sublime_plugin.TextCommand):

    def run(self,edit,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        getFtp(path)
        global FTP
        if(False == FTP):
            return

        FTP.UpLoadFile(path,getRemotePath(path))

    #命令是否可用
    def is_enabled(self,**args):
        return FtpUploadFileCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpUploadFileCommand._check(self,**args)

    #是否允许接收事件（鼠标）参数
    def want_event(self):
        return False

    #
    def _check(self,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        paragrams = {}
        paragrams['path']   = path
        paragrams['command_type']   = 'file'
        paragrams['action'] = 'transfer'

        return valid(**paragrams)


class FtpDownloadFileCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):

        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()
        getFtp(path)
        global FTP
        if(FTP == False):
            return

        FTP.DownLoadFile(path,getRemotePath(path))

    #命令是否可用
    def is_enabled(self,**args):
        return FtpDownloadFileCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpDownloadFileCommand._check(self,**args)

    #是否允许接收事件（鼠标）参数
    def want_event(self):
        return False

    #
    def _check(self,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        paragrams = {}
        paragrams['path']   = path
        paragrams['command_type']   = 'file'
        paragrams['action'] = 'transfer'

        return valid(**paragrams)


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
        return FtpUploadFolderCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpUploadFolderCommand._check(self,**args)

    #
    def _check(self,**args):
        paragrams = {}
        paragrams['path']   = args['paths'][0]
        paragrams['command_type']   = 'folder'
        paragrams['action'] = 'transfer'

        return valid(**paragrams)


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
        return FtpDownloadFolderCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpDownloadFolderCommand._check(self,**args)
    
    #
    def _check(self,**args):
        paragrams = {}
        paragrams['path']   = args['paths'][0]
        paragrams['command_type']   = 'folder'
        paragrams['action'] = 'transfer'

        return valid(**paragrams)


class FtpDiffRemoteFileCommand(sublime_plugin.TextCommand):
    def run(self,edit,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

    #命令是否可用
    def is_enabled(self,**args):
        return False
        # return FtpDiffRemoteFileCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpDiffRemoteFileCommand._check(self,**args)

    #
    def _check(self,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        paragrams = {}
        paragrams['path']   = path
        paragrams['command_type']   = 'file'
        paragrams['action'] = 'transfer'

        return valid(**paragrams)


#Generate a config file for ftp connect
class FtpMapToRemoteCommand(sublime_plugin.TextCommand):

    def run(self,edit,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        if os.path.isfile(path):
            paths = os.path.split(path)
            path  = paths[0]

        conf_dir = os.path.join(path,'ftp-config.json')

        default_conf = open( DEFAULT_CONFIG_PATH,'rb' )
        conf = open(conf_dir,"wb")
        conf.write(default_conf.read())

        default_conf.close()
        conf.close()

    #命令是否可用
    def is_enabled(self,**args):
        return FtpMapToRemoteCommand._check(self,**args)

    #命令是否可见
    def is_visible(self,**args):
        return FtpMapToRemoteCommand._check(self,**args)

    #
    def _check(self,**args):
        try:
            path = args['paths'][0]
        except Exception:
            path = self.view.file_name()

        paragrams = {}
        paragrams['path']   = path
        paragrams['command_type']   = 'none'
        paragrams['action'] = 'config'

        return valid(**paragrams)
