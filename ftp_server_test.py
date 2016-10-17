# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:03:44 2016

@author: root
"""

from socket import *
import os
import sys
import time
import string

lstCmd    = ['dir','ls','exit','bye','quit','clear','cls','get','mget',
            'put','mput','rm','delete','mv','rename','cd','pwd','chmod',
            'cp','copy','?','help','rmdir','mkdir','!','connect','open',
            'close','disconnect']
defPort = 1111
filFlag = '*file*'

class IO:
    def connect(self, host, port):
      try:
        print 'Membuat socket...'
        self.sockIO = socket(AF_INET, SOCK_STREAM)
      except:
        print 'Gagal membuat socket !'
        ret = 0
      else:
        try:
        print 'Koneksi ke ' + host + ' port ' + str(port)
        self.sockIO.connect((host, port))
        except:
        print 'Koneksi gagal!\n\r'
        ret = 0
        else:
        print 'Koneksi sukses...\n\r'
        data = self.sockIO.recv(1024)
        print data
        ret = self.sockIO        
      return ret    

    def sendFile(self,sock,file):
      sock.send(filFlag)
      user = os.environ['USER']
          command = filFlag
      size = os.stat(file)[6]
      f = open(file,'r')
      pos = 0
      while 1:
        if pos == 0:    
            buffer = f.read(5000000-282)
        if not buffer: break
        count = sock.send(command + ':' + \
        string.rjust(os.path.basename(file),214) + ':' + \
            string.rjust(str(size).strip(),30) + ':' + \
            string.rjust(str(user).strip(),30) + \
        buffer)
        pos = 1
        else:
        buffer = f.read(5000000)        
        if not buffer: break
        count = sock.send(buffer)                
    

    def recvFile(self,sock):
    pjg      = 0
    msg1      = sock.recv(283).split(':')
    flag     = msg1[0].strip()
    namafile = msg1[1].strip()
    total     = msg1[2].strip()
    user     = msg1[3].strip()    
    file      = namafile

    if flag == filFlag:
        try:
        f = open(file,'w')
        except:                        
        ret = 0
        print 'Tidak dapat menyimpan file'
        sys.exit()
        else:
        try:
            while 1:        
                leftToRead = int(total) - pjg        
                if not leftToRead: break
                msg = sock.recv(5000000)
            pjg = pjg + len(msg)
            f.write(msg)    
            os.system('echo -n !')
            f.close()    
        except:                
            os.remove(file)            
            ret = 0
        else:
            ret = 1
    
    def close(self):
      self.sockIO.close()
    
class CMD:
    def __init__(self):
      self.getFlag = '*get*'
      self.putFlag = '*put*'
      self.IO      = IO()
      self.isConnected = 0
    
    def checkCmd(self, cmd):
      ret = 0
      cmd0= cmd
      cmd = cmd.strip().split()
      cmd[0] = cmd[0].lower()
    
      if cmd[0] or cmd[0][0] in lstCmd:
        if cmd[0] in ['?','help']:
        print '\n\rDaftar perintah yang digunakan: \n\r\n\r' + \
        '?                   disconnect        mv [file_lama] [file_baru]\n' +\
        'bye            exit            open [host]\n' +\
        'cd [direktori]        get [file]        put [file]\n' +\
        'chmod [mode] [file]    help            pwd\n' +\
        'clear            ls [direktori|file]    rename [file_lama] [file_baru]\n' +\
        'cls            rm [file]        rmdir [direktori]\n' +\
        'connect [host]        mget [files]        quit\n' +\
        'delete [file]        mkdir [direktori]       ![perintah_lokal]\n' +\
        'dir [direktori|file]    mput [files]\n\r'

        elif cmd[0] in ['connect','open']:
        if not self.isConnected:
            if len(cmd) == 2:
            self.Sock = self.IO.connect(cmd[1], defPort)
            if self.Sock <> 0:
                self.isConnected = 1
            else:
                self.isConnected = 0
            else:
            print 'penggunaan: connect|open [host]'
        else:
            print 'Tutup koneksi dulu...'
        
        elif cmd[0] in ['clear','cls']:        
        os.system('clear')        

        elif cmd[0] in ['put']:    
        if self.isConnected:
            if os.path.isfile(cmd[1]):
            ret = 1    
            self.IO.sendFile(self.Sock, cmd[1])
            else:
            print 'Gagal membaca file'
        else:
            print 'penggunaan: put [file]'
            
        elif cmd[0] in ['bye','exit','quit','close','disconnect']:
        if self.isConnected:            
            self.Sock.send(cmd[0])
            self.isConnected = 0
            print self.Sock.recv(100)
            ret = 1    
        else:
            print 'Goodbye...\n\r'
            sys.exit()
    
        elif cmd[0][0] == '!':
        if len(cmd[0]) == 2:            
            if cmd[0][1:] == 'cd':
            print os.chdir(cmd[2])
            else:
            print os.system(cmd0[1:])
        else:
            print os.system(cmd0[1:])            
            
        else:
        try:
            self.Sock.send(cmd0)
            ret = 1
        except:
            print 'Tidak terkoneksi !'
                    
      else:
        print 'Perintah tidak dikenal.'
    
      return ret

    def runCmd(self):
      print '\n\r+ + + DrSlump FTP Client + + +\n\r'
      while 1:
        cmd = raw_input('ftp> ')
        if len(cmd.strip()) > 0:
        ret = self.checkCmd(cmd)
        if self.isConnected and ret == 1:
            data = self.Sock.recv(500000)
            if data[:len(filFlag)] == filFlag:
            ret = self.IO.recvFile(self.Sock)
            if ret == 0:
                print '\n\rFile gagal di download !'
            else:
                print '\n\rFile berhasil di download...'
            else:        
            print data
                            
if __name__ == "__main__":
    cmd = CMD()
    cmd.runCmd()