'''
Created on 13.08.2013

@author: Genji
'''

from PySide.QtCore import QObject
import socket
try:
    import thread
except ImportError:
    import _thread as thread
from struct import unpack
import numpy as np

class DelsysStation(QObject):
    def __init__(self, buffered = False, parent = None):
        super(DelsysStation, self).__init__(parent)
        
        self.host = '192.168.178.22' #'10.16.96.96'
        self.port = 50041
        self.sdkPort = 50040
        self.s = None
        self.sdk = None
        self.buffered = buffered
        if self.buffered:
            self.buffer = np.zeros((16, 10000))
        else:
            self.buffer = None#np.zeros((16, 10000))
        self.exitFlag = True
        
    def start(self):
        self.s = socket.create_connection((self.host, self.port))
        self.sdk = socket.create_connection((self.host, self.sdkPort))
        
        self.sdk.send('START\r\n\r\n')
        self.sdk.recv(1024)
        thread.start_new_thread(self.networking, ())
        
    def networking(self):
        while not self.exitFlag:
            data = np.asarray(unpack('<'+'f'*16*27, self.s.recv(1728)))
            data = np.transpose(data.reshape((-1,16)))
            l = data.shape[1]
            
            if self.buffer is None:
                self.buffer = data
            elif self.buffered:
                self.buffer[:,:-l] = self.buffer[:,l:]
                self.buffer[:,-l:] = data
            else:
                self.buffer = np.hstack((self.buffer, data))
            
    def stop(self):
        self.sdk.send("QUIT\r\n\r\n")
        self.s.close()
        self.sdk.close()
    
    def __del__(self):
        if not self.exitFlag:
            self.exitFlag = True
            self.stop()