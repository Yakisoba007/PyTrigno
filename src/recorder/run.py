'''
Created on 13.08.2013

@author: Genji
'''

import cPickle as pickle
class Run(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        
        self.filename = filename + ".pk"
        self.data = None
        self.triggers = []
    
    def stop(self, data):
        self.data = data
        print self.data.shape
        with open(self.filename, 'wb') as f:
            pickle.dump((self.data, self.triggers), f)
