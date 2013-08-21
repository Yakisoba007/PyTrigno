'''
Created on 19.08.2013

@author: Rachel Hornung
'''

import primesense.openni2 as oni

class KinectRecorder(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        oni.initialize()
        self.dev=oni.Device.open_any()
        self.depth_stream = self.dev.create_depth_stream()
        #self.depth_stream.start();
        self.rgb_stream=self.dev.create_color_stream()
        #self.rgb_stream.start();
        
    def startRecording(self, name):
        self.onirecorder=oni.Recorder(name)
        self.onirecorder.attach(self.depth_stream)
        self.onirecorder.attach(self.rgb_stream)
        self.depth_stream.start()
        self.rgb_stream.start()
        self.onirecorder.start()
       

    def stopRecording(self):
        self.onirecorder.stop()
        self.rgb_stream.stop()
        self.depth_stream.stop()

    def killRecorder(self):
        #self.rgb_stream.stop()
        #self.depth_stream.stop()
        oni.unload()