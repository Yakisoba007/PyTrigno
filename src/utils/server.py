from PySide.QtCore import QObject
import socket
try:
    import thread
except ImportError:
    import _thread as thread
from struct import unpack
import numpy as np

class DelsysStation(QObject):
    '''
    class to receive data from delsys station
    
    connect to station, buffer received data
    '''
    def __init__(self, buffered = False, parent = None):
        super(DelsysStation, self).__init__(parent)
        
        self.host = '10.16.96.96'
        self.dataPort = 50041
        self.accPort = 50042
        self.sdkPort = 50040
        self.emg = None
        self.acc = None
        self.sdk = None
        self.buffered = buffered
        if self.buffered:
            self.buffer = [np.zeros((16, 10000)),  np.zeros((48,10000)) ]
        else:
            self.buffer = [np.zeros((16,0)), np.zeros((48,0))]
        self.exitFlag = True
        
    def start(self):
        ''' establish connection:
        sdk - port
        emg - port
        accelerometer - port
        '''
        print "connect to " + str(self.host)
        self.sdk = socket.create_connection((self.host, self.sdkPort))
        self.emg = socket.create_connection((self.host, self.dataPort))
        self.acc = socket.create_connection((self.host, self.accPort))
        
        print "connected"
        self.sdk.send('START\r\n\r\n')
        self.sdk.recv(1024)
        thread.start_new_thread(self.networking, (self.emg, 0))
        thread.start_new_thread(self.networking, (self.acc, 1))
        
    def networking(self, server, index):
        ''' receive packets of data and fill buffer '''
        shp = (-1,16) if index ==0 else (-1,48)
        while not self.exitFlag:
            data = server.recv(1728)

            l = len(data)
            while l < 1728:
                data += server.recv(1728-l)
                l = len(data)

            data = np.asarray(unpack('<'+'f'*16*27, data))
            data = np.transpose(data.reshape((shp)))
            
            l = data.shape[1]
            if self.buffered:
                self.buffer[index][:,:-l] = self.buffer[index][:,l:]
                self.buffer[index][:,-l:] = data
            else:
                self.buffer[index] = np.hstack((self.buffer[index], data))
            
    def stop(self):
        ''' close connections to server '''
        self.sdk.send("QUIT\r\n\r\n")
        self.emg.close()
        self.sdk.close()
        self.acc.close()
    
    def flush(self):
        ''' reset buffer '''
        self.buffer = [np.zeros((16,0)), np.zeros((48,0))]
    
    def __del__(self):
        ''' delete server after closing all connections '''
        if not self.exitFlag:
            self.exitFlag = True
            self.stop()
