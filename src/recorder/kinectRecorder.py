import primesense.openni2 as oni

class KinectRecorder(object):
    '''
    class to control kinect recording, using openni2 and primesense driver
    
    record depth and rgb stream
    for future use: adjust to only record skeleton
    '''


    def __init__(self):
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