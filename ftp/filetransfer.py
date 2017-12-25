#coding:utf-8
from ctypes import *
import os   
import sys   
import ftplib
import logging


class FileTransfer:

    ftp     = ftplib.FTP()
    bIsDir  = False  
    path    = ""
    conf    = ""

    def __init__( self,conf):
        self.conf = conf
        print(conf['ftp_passive_mode'])
        #Open debug,level's val with 0,1,2.   
        self.ftp.set_debuglevel(2)
        #0 active mode, 1 passive
        self.ftp.set_pasv(conf['ftp_passive_mode'])
        #Connect host
        self.ftp.connect( conf['host'], conf['port'] )

    #Login to remote's server
    def Login( self): 
        self.ftp.login( self.conf['user'],self.conf['password'] ) 

    #Download a file from remote's server
    def DownLoadFile( self, LocalFile, RemoteFile ):
        # if existn't tmp_file.txt new file
        file_handler = open( LocalFile, 'wb' )
        self.ftp.retrbinary( "RETR %s" % ( RemoteFile ), file_handler.write )    
        file_handler.close()
        return True

    #Upload a file to remote's server
    def UpLoadFile( self, LocalFile, RemoteFile ):

        if False == os.path.isfile( LocalFile ):  
            return False
          
        file_handler = open( LocalFile, "rb")
        self.ftp.storbinary( 'STOR %s' % RemoteFile, file_handler, 4096 )
        file_handler.close()  
        return True  

    #Upload a folder to remote's server
    def UpLoadFolder( self, LocalDir, RemoteDir ): 

        if False == os.path.isdir(LocalDir):
            return False
        
        if False == self.isDir(RemoteDir):
            self.ftp.mkd(RemoteDir)

        self.ftp.cwd( RemoteDir )

        LocalNames = os.listdir(LocalDir)
        path = ''
        for file in LocalNames:
            path = os.path.join( LocalDir, file)
            if os.path.isdir( path ):
                self.UpLoadFolder( path, file )
            else:
                self.UpLoadFile( path, file )
                
        self.ftp.cwd( ".." )

    #Download a folder from remote's sever
    def DownLoadFolder( self, LocalDir, RemoteDir ): 

        if False == os.path.isdir( LocalDir ):
            os.makedirs( LocalDir )

        self.ftp.cwd( RemoteDir )

        RemoteNames = self.ftp.nlst()
        path = ''
        for file in RemoteNames:
            path = os.path.join( LocalDir, file ) 
            if self.isDir( file ):
                self.DownLoadFolder( path, file )           
            else:  
                self.DownLoadFile( path, file )

        self.ftp.cwd( ".." )
        return

    #Check whether the remote's path is a directory
    def isDir( self, path ):
        try:
            self.ftp.cwd(path)
        except Exception as e:
            return False
        else:
            self.ftp.cwd('..')
            return True
    # Check connect
    def checkConnect(self):
        try:
            self.ftp.nlst()
        except Exception as e:
            return False
        return True

    #Close ftp connect
    def close( self ): 
        self.ftp.quit()