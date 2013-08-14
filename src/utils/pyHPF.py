'''
Created on 23.05.2013

@author: Genji
'''

class pyHPF(object):
    def __init__(self, ref):
        self.ChannelCount = ref.GetChannelCount()
        self.xmin = ref.GetFirstAvailibleTime()
        self.xmax = ref.GetLastAvailibleTime()
        self.sampling = [ref.GetPerChannelSampleRate(x) for x in range(0, self.ChannelCount)]
        self.data = [ ref.ReadData(x, self.xmin, self.xmax) for x in range(0, self.ChannelCount)]
        self.name = [ ref.GetChannelName(x) for x in range(0, self.ChannelCount)]