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

    def __init__( self, host, port = 21 ):
        #打开调试,级别0,1,2。2显示详细信息   
        self.ftp.set_debuglevel(2)
        self.ftp.set_pasv(0)  #0主动模式 1 #被动模式   
        self.ftp.connect( host, port )

    def Login( self, user, passwd ): 
        self.ftp.login( user, passwd ) 

    def DownLoadFile( self, LocalFile, RemoteFile ):
        file_handler = open( LocalFile, 'wb' )
        self.ftp.retrbinary( "RETR %s" % ( RemoteFile ), file_handler.write )    
        file_handler.close()  
        return True  

    def UpLoadFile( self, LocalFile, RemoteFile ):  
        if os.path.isfile( LocalFile ) == False:  
            return False

          
        file_handler = open( LocalFile, "rb")   
        self.ftp.storbinary( 'STOR %s' % RemoteFile, file_handler, 4096 )  
        file_handler.close()  
        return True  

    def UpLoadFolder( self, LocalDir, RemoteDir ): 
        if os.path.isdir( LocalDir ) == False:  
            return False
        LocalNames = os.listdir( LocalDir )
        self.ftp.cwd( RemoteDir )   
        for Local in LocalNames:   
            src = os.path.join( LocalDir, Local)   
            if os.path.isdir( src ):   
                self.UpLoadFolder( src, Local )   
            else:  
                self.UpLoadFile( src, Local )   
            self.ftp.cwd( ".." )   
        return  

    def DownLoadFolder( self, LocalDir, RemoteDir ): 
        if os.path.isdir( LocalDir ) == False:  
            os.makedirs( LocalDir )
        self.ftp.cwd( RemoteDir )   
        RemoteNames = self.ftp.nlst()  

        for file in RemoteNames:   
            Local = os.path.join( LocalDir, file ) 
            if self.isDir( file ):
                self.DownLoadFolder( Local, file )           
            else:  
                self.DownLoadFile( Local, file )   
            self.ftp.cwd( ".." )   
        return  

    def show( self,list ):
        result = list.lower().split( " " )
        if self.path in result and "<dir>" in result:   
            self.bIsDir = True  

    def isDir( self, path ):
        self.bIsDir = False  
        self.path = path   
        #this ues callback function ,that will change bIsDir value   
        self.ftp.retrlines( 'LIST',self.show )   
        return self.bIsDir  

    #close connect
    def close( self ): 
        self.ftp.quit()  

# ftp = FileTransfer('60.205.34.229')  
# ftp.Login('bxu2442520634','911208Lqmadk')
# ftp.close()
# ftp.DownLoadFile('test.txt', '/htdocs/test.txt')#ok   
# ftp.UpLoadFile('test.txt', '/htdocs/test.txt')#ok   
# ftp.DownLoadFileTree('test/ke', '/ke/te')#ok   
# ftp.UpLoadFileTree('test',"/ke" )   
# ftp.close() 
# print"ok!"