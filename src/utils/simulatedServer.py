'''
Created on 14.08.2013

@author: Genji
'''

import socket
import thread
serverStatus = False
from struct import pack
import numpy as np
import sys

def commandPort():
    global serverStatus
    
    port = 50040
    portData = 50041
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sData= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sAcc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.bind(('', port))
    s.listen(1)
    print "ich warte"
    conn, _ = s.accept()
    
    sData.bind(('', portData))
    sData.listen(1)
    connData, _ = sData.accept()
    
    sAcc.bind(('', portData+1))
    sAcc.listen(1)
    connAcc, _ = sAcc.accept()    
    while True:
        data = conn.recv(1024)
        if not data: break
        if not serverStatus and data in ('START\r\n\r\n'):
            serverStatus = True
            conn.sendall('accepted')
            thread.start_new_thread(sendData, (connData,))
            thread.start_new_thread(sendData, (connAcc,))
        if serverStatus and data in ('QUIT\r\n\r\n'):
            serverStatus = False
            break
    s.close()
    sData.close()
    sAcc.close()
def sendData(conn):
    while serverStatus:
        package = ''
        accpkg = ''
        data = np.random.rand(16)
        for i in range(data.shape[0]):
            package += pack('<'+'f', data[i])
        conn.sendall(package)
if __name__ == '__main__':
    commandPort()