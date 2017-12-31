#coding:utf-8
import os
import sys
import ftplib
import difflib
import sublime

class FileTransfer:
    aftp         = ftplib.FTP()
    bIsDir       = False
    path         = ""
    conf         = ""
    plugin_cache = ""
    local_path   = ""

    def __init__( self,conf):
        self.plugin_cache = os.path.join(sublime.cache_path(),'AFTP')
        self.conf = conf
        #Open debug,level's val with 0,1,2.
        self.aftp.set_debuglevel(1)
        #0 active mode, 1 passive
        self.aftp.set_pasv(conf['ftp_passive_mode'])
        #Connect host
        self.aftp.connect( conf['host'], conf['port'] )

    #Login to remote's server
    def Login( self):
        self.aftp.login( self.conf['user'],self.conf['password'] )

    #Download a file from remote's server
    def DownloadFile( self, LocalFile, RemoteFile ):
        dir_tmp  = os.path.splitext(LocalFile)
        tmp_file = os.path.join(self.plugin_cache,'7821214dssddsd'+dir_tmp[1])
        file_buffer = open(tmp_file,'wb')

        try:
            self.aftp.retrbinary( "RETR %s" % ( RemoteFile ), file_buffer.write )
            file_buffer.close()

            file_buffer  = open(tmp_file,'rb');
            file_handler = open( LocalFile, 'wb' )
            file_handler.write(file_buffer.read())
            file_handler.close()
            file_buffer.close()
        except Exception:
            file_buffer.close()

    #Upload a file to remote's server
    def UploadFile( self, LocalFile, RemoteFile ):
        if False == os.path.isfile( LocalFile ):
            return False
        try:
            ignore = self.conf['ignore']
            if os.path.split(LocalFile)[1] in ignore:
                return
        except Exception:
            pass

        file_handler = open( LocalFile, "rb")
        self.aftp.storbinary( 'STOR %s' % RemoteFile, file_handler, 4096 )
        file_handler.close()

    def DeleteRemoteFile(self,LocalFile,RemoteDir):
        if True == self.isDir(RemoteDir):
            return False
        try:
            self.aftp.delete(RemoteDir)
        except Exception:
            pass

    #Upload a folder to remote's server
    def UploadFolder( self, LocalDir, RemoteDir ):
        if False == os.path.isdir(LocalDir):
            return False

        try:
            ignore = self.conf['ignore']
        except:
            ignore = []
            pass

        for ignore_file in ignore:
            if -1 != ignore_file.find('/'):
                if ignore_file[-1] != '/':
                    ignore_file = ignore_file + '/'
                ignore_file = ignore_file.replace("/",os.path.sep)
                if os.path.join(self.conf['local_path'],ignore_file) == LocalDir + os.path.sep:
                    return
        if False == self.isDir(RemoteDir):
            self.aftp.mkd(RemoteDir)

        self.aftp.cwd( RemoteDir )

        LocalNames = os.listdir(LocalDir)
        path = ''
        for file in LocalNames:
            path = os.path.join( LocalDir, file)
            if os.path.isdir( path ):
                self.UploadFolder( path, file )
            else:
                self.UploadFile( path, file )

        self.aftp.cwd( ".." )

    #Download a folder from remote's sever
    def DownloadFolder( self, LocalDir, RemoteDir ):

        if False == os.path.isdir( LocalDir ):
            os.makedirs( LocalDir )

        self.aftp.cwd( RemoteDir )

        RemoteNames = self.aftp.nlst()
        path = ''
        for file in RemoteNames:
            path = os.path.join( LocalDir, file )
            if self.isDir( file ):
                self.DownloadFolder( path, file )
            else:
                self.DownloadFile( path, file )

        self.aftp.cwd( ".." )

    #Delete a folder from remote's server
    def DeleteRemoteFolder( self, LocalDir, RemoteDir ):
        if False == self.isDir(RemoteDir):
            return False

        self.aftp.cwd( RemoteDir )
        RemoteNames = self.aftp.nlst()

        for file in RemoteNames:
            if self.isDir( file ):
                self.DeleteRemoteFolder( LocalDir, file )
            else:
                self.DeleteRemoteFile(LocalDir,file)

        self.aftp.cwd('..')
        self.__destoryFolder(RemoteDir)
        return True

    # Compare file local with remote
    def DiffRemoteFile(self,LocalDir,RemoteDir):
        if False == os.path.isfile(LocalDir):
            return False

        file_extension  = os.path.splitext(LocalDir)
        file_name       = os.path.split(LocalDir)
        tmp_file        = os.path.join(self.plugin_cache,'10xsdfs00diff'+file_extension[1])
        diff_path       = os.path.join(self.plugin_cache,'(remote)'+file_name[1]+'--(local)'+file_name[1])

        self.DownloadFile(tmp_file,RemoteDir)

        text1_lines = self.readfile(tmp_file)
        text2_lines = self.readfile(LocalDir)

        diff_result   = difflib.ndiff(text1_lines, text2_lines)
        diff_result     = ''.join(diff_result)
        diff_byte     = (''.join(diff_result)).encode(encoding='utf-8')

        diff_file = open(diff_path,'wb')
        diff_file.write(diff_byte)
        diff_file.close()

        diff_view     = sublime.active_window().open_file(diff_path)
        diff_view.set_scratch(True)

        try:
            os.remove(diff_path)
        except Exception:
            pass
        try:
            os.remove(tmp_file)
        except Exception:
            pass

    # Delete remote folder
    def __destoryFolder(self,path):
        try:
            self.aftp.rmd(path)
        except Exception:
            pass

    # Check whether the remote's path is a directory
    def isDir( self, path ):
        try:
            self.aftp.cwd(path)
        except Exception as e:
            return False
        else:
            self.aftp.cwd('..')
            return True

    # Check connect is enable
    def checkConnect(self):
        try:
            self.aftp.nlst()
        except Exception as e:
            return False
        return True

    # Check remote folder is empty
    def __isEmptyFloder(self,path):
        files = self.aftp.nlst()
        for file in files:
            return False
        return True
        
    #Close ftp connect
    def close( self ):
        self.aftp.quit()

    # Load file content
    def readfile(self,filename):
        try:
            with open(filename, 'r',encoding = 'utf-8') as fileHandle:
                text = fileHandle.read().splitlines(keepends=True)
            return text
        except IOError as e:
            sys.exit()