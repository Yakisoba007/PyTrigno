class Interactor(object):
    '''
    class to edit triggers inside plots:
     - enter edit mode by pressing button
     - left click on trigger: change position
     - right click on trigger: delete trigger
     - left click on empty: add trigger (on release position)
    to save changes, press button again and choose file to
    save new data into
    
    bounding box for triggers (in order to click triggers more easily)
    is adjusted depending on the zoom factor
    '''


    def __init__(self, canvas, axes, triggers, lines, maxLength):
        self.canvas = canvas
        self.axes = axes
        self.triggers = triggers
        self.lines = lines
        
        #######################################
        # if updating triggers, only triggers #
        # have to be drawn again              #
        # see:                                #
        # http://wiki.scipy.org/Cookbook/Matplotlib/Animations#head-3d51654b8306b1585664e7fe060a60fc76e5aa08
        #######################################
        self.backgrounds = [self.canvas.copy_from_bbox(x.bbox) for x in self.axes]
        
        #################################
        # set mouse events to functions #
        #################################
        self.canvas.mpl_connect('button_press_event', self.onButtonPressed)
        self.canvas.mpl_connect('button_release_event', self.onButtonReleased)
        self.canvas.mpl_connect('motion_notify_event', self.onMotion)
        
        self.drag = False
        self.max = maxLength
        self.draggedTrigger = None
        
    def contains(self, xdata, ax):
        ''' check if xdata is inside bounding box
        of trigger
        
        bounding box depends on the current zoom factor
        '''
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
        ''' add a trigger and draw it on canvas '''
        for i in range(2):
            height = self.lines[i][self.triggers[0]].get_data()[1]
            self.lines[i][xdata], = self.axes[i].plot([xdata]*2, 
                                                    height, c='k', animated = True)
        self.triggers.append(xdata)
        self.canvas.draw()

    def deleteTrigger(self, xdata):
        ''' remove trigger from list and canvas '''
        for i in range(2):
            self.lines[i].pop(xdata)
        self.triggers.remove(xdata)
        self.canvas.draw()
        
    def onButtonPressed(self, event):
        ''' evaluate button pressed events:
         - left: drag mode for clicked trigger
         - right: remove trigger
        '''
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
        ''' evaluate button release event:
         - right: do nothing
         - left in drag mode:
            - exit drag mode
            - update trigger list
            - redraw canvas
         - left not in drag mode: add trigger
        '''
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
        ''' while in drag mode and left mouse button clicked
        redraw canvas and trigger position according
        to mouse movement
        '''
        if event.button != 1: return
        if event.inaxes == None: return
        if not self.drag: return
        for i in range(2):
            self.lines[i][self.draggedTrigger].set_xdata(event.xdata)
        self.canvas.draw()
