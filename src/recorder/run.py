try: 
    import cPickle as pickle
except ImportError:
    import pickle as pickle
    
class Run(object):
    '''
    container class to hold recorded data and triggers
    dump them when recording is stopped
    '''


    def __init__(self, filename):
        self.filename = filename + ".pk"
        self.data = None
        self.triggers = []
    
    def stop(self, data):
        self.data = data
        print len(self.data)
        print self.data[0].shape
        with open(self.filename, 'wb') as f:
            pickle.dump((self.data, self.triggers), f)
