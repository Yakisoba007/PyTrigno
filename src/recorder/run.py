'''
Created on 13.08.2013

@author: Genji
'''
try: 
    import cPickle as pickle
except ImportError:
    import pickle as pickle
    
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
        print len(self.data)
        print self.data[0].shape
        with open(self.filename, 'wb') as f:
            pickle.dump((self.data, self.triggers), f)
