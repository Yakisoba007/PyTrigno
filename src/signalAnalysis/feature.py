import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import RectangleSelector
from utils import selector

def moving_integrate(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n-1:] = ret[n-1:] - ret[:1-n]
    ret[:n-1] = np.nan
    return ret

def moving_average(a, n=3):
    ret = moving_integrate(a, n)/n
    return ret

def rootMeanSquare(a, n=3):
    ret = np.cumsum(a**2, dtype=float)
    ret[n-1:] = ret[n-1:] - ret[:1-n]
    ret[:n-1] = np.nan
    ret = np.sqrt(ret/n)
    return ret

def medianFrequency(y, f):
    f_median = np.cumsum(y)
    f_median = f_median/max(f_median)
    f_median = f[np.where(f_median>=0.5)[0][0]]
    return f_median

def meanFrequency(y, f):
    return (np.cumsum(f*y)/np.cumsum(y))[-1]

def rootMeanSquareDifference(f, s):
    ret = np.sqrt(np.sum((f-s)**2)/len(f))
    return ret

def signalPlot(time, data, names):
    plt.figure(1)
    colors =['r', '#FCBDB1', 'g', '#B6FAC4', 'b', '#CAB6FA', 'c']
    ax = plt.subplot(111)
    for x in range(len(data)):
        ax.plot(time, data[x], c=colors[x], label=names[x])
    plt.legend()
    selector.keyPressed.RS = RectangleSelector(ax, selector.onselect, drawtype='box', rectprops=dict(facecolor='red', edgecolor = 'black',
                 alpha=0.5, fill=True))
    plt.connect('key_press_event', selector.keyPressed)
    plt.show()
    plt.show()
#    plt.figure(1)
#    plt.subplot(211)
#    plt.plot(time, sg_emg, 'g', time, mav, 'r', time, rms, 'b')
#    plt.legend(('filtered emg', 'mav', 'rms'))
#    plt.subplot(212)
#    plt.plot(y_pwr[0], y_pwr[1], label='power spectrum [V**2/Hz]')
#    plt.plot([f_mean, f_mean],[0, max(y_pwr[1])], 'r', label='f_mean: '+str(f_mean))
#    plt.plot([f_median, f_median],[0, max(y_pwr[1])], 'g', label='f_median: '+str(f_median))
#    plt.legend()
#    pp.savefig()
#    
#    plt.figure(2)
#    plt.subplot(211)
#    plt.plot(time, sg_emg, 'g', time, mmav1, time, mmav2, 'r')  
#    plt.legend(('filtered emg', 'mmav1', 'mmav2'))
#    plt.subplot(212)
#    plt.plot(ff, y_amp, label='amplitude spectrum')
#    plt.plot([f_mmean, f_mmean],[0, max(y_amp)], 'r', label='f_mmean: '+str(f_mmean))
#    plt.plot([f_mmedian, f_mmedian],[0, max(y_amp)], 'g', label='f_mmedian: '+str(f_mmedian))
#    plt.legend()
#    pp.savefig()
#    
#    plt.figure(3)
#    plt.hist(sg_emg, 50)
#    pp.savefig()
#    
#    pp.close()
#    plt.show()
def featurePosPlot(featureList, name, k=1, save=None):
    font = {'family' : 'monospace',
        'weight' : 'normal',
        'size'   : '6'}
    plt.rc('font', **font)
    fig = plt.figure(k)
    fig.suptitle(name)
    ax = fig.add_subplot(221)
    sc = ax.scatter([2,2,3,3,3,2], [3,1,1,2,3,2], c=featureList['mav'], s=1000, cmap=cm.get_cmap('binary'))
    ax.set_title("mav")
    plt.colorbar(sc, ticks = featureList['mav'])
    ax.grid(True)
    ax = fig.add_subplot(224)
    sc = ax.scatter([2,2,3,3,3,2], [3,1,1,2,3,2], c=featureList['ni'], s=1000, cmap=cm.get_cmap('binary'))
    ax.set_title("ni")
    plt.colorbar(sc, ticks = featureList['ni'])
    ax.grid(True)
    
    ax = fig.add_subplot(222)
    sc = ax.scatter([2,2,3,3,3,2], [3,1,1,2,3,2], c=featureList['rmsd'], s=1000, cmap=cm.get_cmap('binary'))
    plt.colorbar(sc, ticks = featureList['rmsd'])
    ax.set_title("rmsd")
    ax.grid(True)
    ax = fig.add_subplot(223)
    sc = ax.scatter([2,2,3,3,3,2], [3,1,1,2,3,2], c=featureList['var'], s=1000, cmap=cm.get_cmap('binary'))
    ax.set_title("var")
    plt.colorbar(sc, ticks = featureList['var'])
    ax.grid(True)
    
    if save:
        save.savefig(k)
    else:
        plt.show()

def plotShortLong(datasets, runNames):
    xmax = 0
    for x in (0,5):
        tmax = np.nanmax(datasets[x][1])
        if tmax > xmax:
            xmax = tmax
    print xmax
    for i in (0, 2, 1, 3):
        plt.figure(i)
        title = 'short ' if i < 2 else 'long '
        title = title + 'oben' if i%2 > 0 else title+ 'unten'
        plt.suptitle(title)
        for x in (0,5):
            plt.subplot(2,1,x/3+1)
            plt.gca().set_title(runNames[x])
            plt.plot(datasets[x][1][i])
            plt.ylim((-xmax, xmax))
    plt.show()
        
def featureQuantyPlot(featureList, names, N, save=None):
    color = ['b', 'r', '#FCBDB1', '#B6FAC4', '#CAB6FA', 'g']
    label = ['1', '3', '4', '5', '6', '7']
    figID = 1
    for key in featureList[0].iterkeys():
        fig = plt.figure(figID)
        fig.clf()
        fig.suptitle(key)
        for k in range(N):
            for i in range(len(featureList[k][key])):
                plt.plot([k], featureList[k][key][i], 'o', color=color[i], markersize=10, label=label[i])
            plt.grid(True)
            plt.xticks( range(len(featureList[k][key])), names, rotation=10 )
        plt.gca().set_xlim(-0.5, N-0.5)
        plt.legend(label)
        if save:
            save.savefig(figID) 
        else:
            plt.show()
        figID += 1