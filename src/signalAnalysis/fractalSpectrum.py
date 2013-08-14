'''
Created on 10.07.2013

@author: Genji
'''
import numpy as np
import matplotlib.pyplot as plt
import h5py
from numpy.core.numeric import dtype
from matplotlib.backends.backend_pdf import PdfPages
from scipy.signal import resample
#d = datas

def qOrderHurstExponent(x, scale, qOrder, polyOrder):
    fq = np.zeros((len(qOrder), len(scale)))
    for ns in range(len(scale)):
        seg = int(np.floor(len(x)/scale[ns]))
        rms = np.zeros((seg,))
        for v in range(seg):
            index = range(int(v*scale[ns]), int((v+1)*scale[ns])) #+/- 1????????????????????????
            p = np.poly1d(np.polyfit(index, x[index], polyOrder))
            fit = p(index)
            rms[v] = np.sqrt(np.mean( (x[index] - fit)**2) )
        
        for nq in range(len(qOrder)):
            qRms = rms**qOrder[nq]
            fq[nq, ns] = np.mean(qRms)**(1.0/qOrder[nq])
        fq[np.where(qOrder==0), ns] = np.exp(0.5*np.mean(np.log(rms**2)))
    
    Hq = np.zeros((len(qOrder), 2))
    for nq in range(len(qOrder)):
        p = np.polyfit(np.log2(scale), np.log2(fq[nq, :]), 1)
        Hq[nq] = p
    return Hq
        
def localHurstExponent(x, Hq, halfmax, scale, qOrder, polyOrder):
    timeIndex = range(halfmax, len(x)-halfmax)
    rms = []
    for ns in range(len(scale)):
        halfseg = int(np.floor(scale[ns]/2.0))
        rms.append(np.zeros(len(x)))
        for v in timeIndex:
            index = range(v-halfseg, v+halfseg+1)
            p = np.poly1d(np.polyfit(index, x[index], polyOrder))
            fit = p(index)
            rms[ns][v] = np.sqrt(np.mean((x[index]-fit)**2))
    p = np.poly1d(Hq[np.where(qOrder==0)][0])
    reg = p(np.log2(scale))
    Ht = [None]*len(scale)
    for ns in range(len(scale)):
        resRms = reg[ns] - np.log2(rms[ns][timeIndex])
        logScale = np.log2(len(timeIndex)) - np.log2(scale[ns])
        Ht[ns] = resRms/logScale + Hq[np.where(qOrder==0), 0][0]
    return Ht

if __name__ == '__main__':
    #pdfPos = PdfPages('D:\\Master\\emg\\electrodes\\sl 2\\results\\anwinkeln-oft.pdf')
    raw = h5py.File("/media/Kaze/Master/emg/tsne/april2013.hd5")#'D:\\Master\\emg\\tsne\\april2013.hd5')
    datas = np.asarray(raw['pure']['3']['emg'])
    colors = ['b', '#CAB6FA', 'r', '#FCBDB1', '#B6FAC4','g',  'c']
    #for i in range(len(datas)/6):
    #    plt.figure(i)
    
    scmin = 16; scmax=1024; scres=19
    exponent = np.linspace(np.log2(scmin), np.log2(scmax), scres)
    scl = np.round(2.0**exponent)
    scl2 = range(7,19,2)
    m = 2
    q = np.linspace(-5,5,11)
    hm = int(np.floor(max(scl2)/2.0))
    for k in [0, 2, 4]:
        d = np.cumsum(resample(np.asarray(datas[:,k]), len(datas)/10))
        
        Hq = qOrderHurstExponent(d, scl, q, m)
        Ht = localHurstExponent(d, Hq, hm, scl2, q, m)
        Ht_flat = np.transpose(np.asarray(Ht)).reshape(-1)
        binNumber = round(np.sqrt(len(Ht_flat)))
        freq, Htbins = np.histogram(Ht_flat, binNumber)#, density =True)
        ph = freq/max(freq)
        dh = 1-(np.log(ph)/-np.log(np.mean(scl2)))
        plt.subplot(311)
        plt.plot(datas[:,k], c=colors[k])
        plt.subplot(313)
        plt.plot(Htbins[:-1], dh , c=colors[k])
        plt.subplot(312)
        plt.plot(Ht[4], c=colors[k])
    plt.show()
    #    pdfPos.savefig(i)
    #pdfPos.close()
    #plt.close('all')
