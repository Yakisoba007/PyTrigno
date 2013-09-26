'''
Created on 27.08.2013

@author: genji
'''

class Interactor(object):
    '''
    classdocs
    '''


    def __init__(self, canvas, axes, triggers, lines, maxLength):
        '''
        Constructor
        '''
        self.canvas = canvas
        self.axes = axes
        self.triggers = triggers
        self.lines = lines
        self.backgrounds = [self.canvas.copy_from_bbox(x.bbox) for x in self.axes]
        
        self.canvas.mpl_connect('button_press_event', self.onButtonPressed)
        self.canvas.mpl_connect('button_release_event', self.onButtonReleased)
        self.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.drag = False
        self.max = maxLength
        self.draggedTrigger = None
        
    def contains(self, xdata, ax):
        epsilon = 5
        px = (ax.get_xlim()[1]-ax.get_xlim()[0])
        w =  ax.bbox.bounds[2]
        epsilon = px*epsilon/w
        for t in self.triggers:
            print xdata, t
            if xdata > t-epsilon and xdata < t+epsilon:
                return t
        return None

    def addTrigger(self, xdata):
        for i in range(2):
            height = self.lines[i][self.triggers[0]].get_data()[1]
            self.lines[i][xdata], = self.axes[i].plot([xdata]*2, 
                                                    height, c='k', animated = True)
        self.triggers.append(xdata)
        self.canvas.draw()

    def deleteTrigger(self, xdata):
        for i in range(2):
            self.lines[i].pop(xdata)
        self.triggers.remove(xdata)
        self.canvas.draw()
        
    def onButtonPressed(self, event):
        if event.inaxes == None: return
        t = self.contains(event.xdata, event.inaxes)
        if event.button == 1: 
            
            if t is not None:
                self.drag = True
                self.draggedTrigger = t
            else:
                self.drag = False
        elif event.button == 3:
            if t is not None:
                self.deleteTrigger(t)
    
    def onButtonReleased(self, event):
        if event.button != 1: return
        if event.inaxes == None: return
        if self.drag:
            self.drag = False
            idx = self.triggers.index(self.draggedTrigger)
            self.triggers[idx] = event.xdata
            
            for i in range(2):
                line = self.lines[i].pop(self.draggedTrigger)
                self.lines[i][event.xdata] = line
            self.draggedTrigger = None
            
        else:
            self.addTrigger(event.xdata)
    
    def onMotion(self, event):
        if event.button != 1: return
        if event.inaxes == None: return
        if not self.drag: return
        for i in range(2):
            self.lines[i][self.draggedTrigger].set_xdata(event.xdata)
        self.canvas.draw()
