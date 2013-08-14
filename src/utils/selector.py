from matplotlib.patches import Rectangle

xmin = [None]
xmax = [None]
ax = None
rect = None
def init(axis):
    global ax
    global rect
    ax = axis
    rect = Rectangle((0,0), 0, 2, facecolor='0.7')
    ax.add_patch(rect)

def onselect(eclick, erelease):
    'eclick and erelease are matplotlib events at press and release'
    global xmin, xmax
    global ax, rect
    
    xmin[-1] = int(eclick.xdata)
    xmax[-1] = int(erelease.xdata)
    if xmin[-1] > xmax[-1]:
            xmin[-1], xmax[-1]= xmax[-1], xmin[-1]
    
    rect.set_xy((xmin[-1], -1))
    rect.set_width(xmax[-1]-xmin[-1])
    ax.figure.canvas.draw()
    

def keyPressed(event):
    print ' Key pressed.'
    print event.key
    global xmin, xmax
    
    if event.key in ['alt+Q', 'alt+q']:
        if keyPressed.RS.active:
            keyPressed.RS.set_active(False)
        else:
            keyPressed.RS.set_active(True)
    if event.key in ['alt+r', 'alt+R'] and keyPressed.RS.active:
        print "Add selection [" + str(xmin[-1]) + ":" + str(xmax[-1]) + "]"
        xmin.append(None)
        xmax.append(None)
        