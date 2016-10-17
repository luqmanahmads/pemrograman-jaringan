from socket import *
import commands
import os
import sys
import time
import string

lstCmd = ['dir', 'ls', 'exit', 'bye', 'quit', 'get', 'mget', 'put', 'mput', 'rm', 'delete', 'mv', 'rename', 'cd', 'pwd', 'chmod', 'cp', 'copy', 'rmdir', 'mkdir', 'close', 'disconnect']
hostIP = '127.0.0.1'
hostPort = 1111
fileFlag = '*file*'
getFlag = 'get'

class CMD:
    def __init__(self):
        self.byeFlag = '*bye*'

    def checkCmd(self, cmd):
        ret = ''
        cmd = cmd.strip().split()
           cmd[0] = cmd[0].lower()
           
           if cmd[0] in lstCmd:
               if cmd[0] in ['ls', 'dir']:
                   if len(cmd) == 1:
                       cmdS = 'ls -al'
                   else:
                       cmdS = 'ls' + ' ' + cmd[1]
                   ret = commands.getoutput(cmdS)
               
               elif cmd[0] in ['rm', 'delete']:
                   if len(cmd) == 2:
                       ret = commands.getoutput('rm ' + cmd[1])
                       if ret == '':
                           ret = 'File ' + cmd[1] + ' telah di hapus.'
                   else:
                       ret = 'penggunaan: rm|delete [file].'
                           
               elif cmd[0] in ['rmdir']:
                   if len(cmd) == 2:
                       ret = commands.getoutput('rm -rf ' + cmd[1])
                       if ret = '':
                           ret = 'Direktori ' + cmd[1] + ' telah dihapus.'
                   else:
                       ret = 'rmdir [direktori].'
               
               elif cmd[0] in ['mkdir']:
                   if len(cmd) == 2:
                       ret = commands.getoutput('mkdir ' + cmd[1])
                       if ret == '':
                           ret = 'Direktori ' + cmd[1] + ' telah dibuat.'
                   else:
                       ret = 'penggunaan: mkdir [direktori].'

               elif cmd[0] in ['mv', 'rename']:
                   if len(cmd) == 3:
                       ret = commands.getoutput('mv ' + cmd[1] + ' ' + cmd[2])
                   else:
                       ret = 'penggunaan: mv|rename [file_lama] [file_baru].'
                       
               elif cmd[0] in ['cp', 'copy']:
                   if len(cmd) == 3:
                       ret = commands.getoutput('cp ' + cmd[1] + ' ' + cmd[2])
                   else:
                       ret = 'penggunaan: cp|copy [file_sumber] [file_tujuan].'
                       
               elif cmd[0] in ['chmod']:
                   if len(cmd) == 3:
                       ret = commands.getoutput('chmod ' + cmd[1] + ' ' + cmd[2])
                       if ret == '':
                           ret = 'Hak akses ' + cmd[1] + ' telah di ubah.'
                       else:
                           ret = 'penggunaan: chmod [mode] [file].'
                           
               elif cmd[0] in ['cd']:
                   if len(cmd) == 2:
                       try:
                           os.chdir(cmd[1])
                       except:
                           ret = 'Direktori tidak ada.'
                       else:
                           ret = 'Direktori sekarang ' + os.getcwd()
                   else:
                       ret = 'penggunaan: cd [direktori]
                   
               elif cmd[0] in ['pwd']:
                   ret = 'Direktori sekarang ' + commands.getoutput('pwd')
                   
               elif cmd[0] in ['bye', 'exit', 'quit', 'close', 'disconnect']:
                   ret = self.byeFlag
        return ret
        
class CLI:
    def __init__(self):
        self.cmd = CMD()
        self.childLst = []
        
    def updatePid(self, pids):
        while self.childLst:
            pid, status = os.waitpid(0, os.WNOHANG)
            if not pid : break:
            pids.remove(pid)
                   
    def sendFile(self,sock, file):
        sock.send(filFlag)
        user = os.environ['USER']
        command = filFlag
        size = os.stat(file)[6]
        try:
            f = open(file,'r')
        except:
            ret = 0
        else:
            pos = 0
            while 1:
                if pos == 0:
                    buffer = f.read(5000000-282)
                    if not buffer: break:
                    count = sock.send(command + ':' + \
                    string.rjust(os.path.basename(file), 214) + ':' + \
                    string.rjust(str(size).strip(),30) + ':' + \
                    string.rjust(str(user).strip(),30) + \
                    buffer)
                    pos = 1
                else:
                    buffer = f.read(5000000)
                    if not buffer: break:
                    count = sock.send(buffer)
            ret = 1
        return ret