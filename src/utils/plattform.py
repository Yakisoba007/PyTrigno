'''
Created on 22.07.2013

@author: genji
'''

import platform
import os
if platform.system() == 'Linux':
    partition = '\\media\\Kaze\\'
elif platform.system() == 'Windows':
    partition = 'D:\\'
else:
    print "platform not supported"

import os
def fixpath(path):
    if platform.system() == 'Linux':
        path = '\\media\\Kaze\\' + path[3:]
        x = path.split('\\')
        rt = '/'.join(x)
    else:
        rt = path
    return rt