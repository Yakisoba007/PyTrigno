'''
Created on 21.08.2013

@author: Genji
'''
import sys
import pyHPF
sys.modules['pyHPF'] = pyHPF

#import primesense.openni2 as oni
import primesense.openni2 as oni

import numpy as np
import thread
import ctypes

class extendedPyHPF(pyHPF.pyHPF):
    '''
    data wrapper for multiple input format
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        l = data[0][0].shape
        self.data = [None]*l[0]*4
        self.name = []
        for i in range(l[1]):
            name = str(i+1).zfill(2)
            for k in ('emg ', 'accX ', 'accY ', 'accZ '):
                self.name.append(k + name)
        self.data[::4] = data[0][0].tolist()
        for i in range(l[0]):
            for k in range(1,4):
                self.data[i*4+k] = data[0][1][i+k-1].tolist()
        self.triggers = data[1]
        
        if len(data) == 3:
            oni.initialize()
            try:
                self.dev = oni.Device.open_file(data[2])
            except:
                print "could not open oni-file, no oni-file will be loaded"
                return 
            self.depth_stream = self.dev.create_depth_stream()
            self.clr_stream = self.dev.create_color_stream()
            self.frames = {}
            self.player = oni.PlaybackSupport(self.dev)
            
    def seekFrame(self, idx):
        if idx == -1:
            self.frames = {}
        
        self.depth_stream.start()
        self.clr_stream.start()

        if idx >= self.depth_stream.get_number_of_frames():
            idx = self.depth_stream.get_number_of_frames()-1
        
        if idx not in self.frames:
            self.player.seek(self.depth_stream,idx)
            frame = self.clr_stream.read_frame()
            frame = np.ctypeslib.as_array(frame.get_buffer_as_triplet())
            #np.asarray(list(frame.get_buffer_as_triplet()))
            frame = frame.reshape((480,640,3))
            frame = np.mean(frame, axis=2)
            self.frames[idx] = np.flipud(frame).transpose()
            
#            frame = self.depth_stream.read_frame()
#            frame = np.asarray(list(frame.get_buffer_as_uint16()))
#            self.frames[idx] = frame.reshape((480,640)).transpose()
        return self.frames[idx]
#        for i in range(max):
#            frame = self.depth_stream.read_frame()
#            frame = np.asarray(list(frame.get_buffer_as_uint16()))
#            self.frames[i] = frame.reshape((480,640))
#        print self.frames
#        print self.frames.shape
#        self.depth_stream.stop()
#        self.clr_stream.stop()
#        oni.unload()
