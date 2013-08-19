'''
Created on 13.08.2013

@author: Genji
'''
from run import Run
import os

class Session(object):
    '''
    classdocs
    '''


    def __init__(self, name, remarks, outDir):
        '''
        Constructor
        '''
        self.name = name
        self.remarks = remarks
        self.dir = outDir
        self.runs = []
        self.dump("ReadMe.txt")
        
    def addRun(self, name):
        self.runs.append(Run(os.path.join(self.dir, name)))

    def stopRun(self, data):
        self.runs[-1].stop(data)
        
    def addTrigger(self, time):
        self.runs[-1].triggers.append(time)
        
    def dump(self, filename):
        with open(os.path.join(self.dir,filename), 'w') as f:
            f.write(self.remarks)
            f.close()