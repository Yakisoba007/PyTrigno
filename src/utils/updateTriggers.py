import cPickle as pickle
import sys

def save(triggers, fileName):
    files = sys.argv
    with open(fileName, 'rb') as ifile:
        tmp = pickle.load(ifile)
    ret = (tmp[0], triggers)
    with open(fileName, 'wb') as ofile:
        pickle.dump(ret, ofile)