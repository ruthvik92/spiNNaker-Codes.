
###took the function from Garibaldi, Liu Qi, Steve furbers paper.

import math
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
file_name = "/home/ruthvik/Desktop/Summer 2017/00027.aedat"
image_size = 28
jaer_size =0
def aerfile_to_spike(file_name, image_size, jaer_size):
    
    '''Reads an AER file and converts it to a couple of PyNN SpikeSourceArrays.
        :param file_name: Name of the file to open
        :param image_size: Width and height of the image
        :param jaer_size: -Not used?-
        
        :returns: A spike array for each polarity
    '''
    if os.path.exists(file_name):
        f = open(file_name,'r')
        for i in range(5):
            f.readline()
        All = np.fromfile(f, dtype='>u4')
        All = np.transpose(np.reshape(All,(All.shape[0]/2 , 2)))
        AllTs = np.uint32(All[1])
        AllTs = AllTs.astype(float)/1000.
        AllAddr = np.uint32(All[0])

        xmask = 254 #hex2dec ('fE')  x are 7 bits (64 cols) ranging from bit 1-7
        ymask = 32512 #hex2dec ('7f00')  y are also 7 bits ranging from bit 8 to 14.
        xshift=1 # bits to shift x to right
        yshift=8 # bits to shift y to right
        polmask=1 # polarity bit is LSB


        pol= (AllAddr & polmask) # 0 is on, 1(Polirity = -1) is off 
        AllAddr = AllAddr + pol
        x=(AllAddr & xmask) >> xshift
        y=(AllAddr & ymask) >> yshift
        neuron_id = y*image_size+x
        #print pol
        spike_source_array_on = [[] for i in range(image_size*image_size)]
        spike_source_array_off = [[] for i in range(image_size*image_size)]
        for i in range(image_size*image_size):
            index_i = np.where(neuron_id == i)[0]
            index_on = np.where(pol[index_i] == 0)[0]
            index_off = np.where(pol[index_i] == 1)[0]
            if len(index_on) > 0:
                spike_source_array_on[i] = AllTs[index_i[index_on]].tolist()
            if len(index_off) > 0:
                spike_source_array_off[i] = AllTs[index_i[index_off]].tolist()
        return spike_source_array_on, spike_source_array_off
    
    else:
        return [], []

def raster_plot_spike(spikes, marker, markersize=4):
    '''Plot PyNN SpikeSourceArrays
        :param spikes: The array containing spikes
    '''
    x = []
    y = []
    
    for neuron_id in range(len(spikes)):
        for t in spikes[neuron_id]:
            x.append(t)
            y.append(neuron_id)
    
    plt.plot(x, y, marker, markersize=markersize)


on, off = aerfile_to_spike(file_name, image_size, jaer_size)
raster_plot_spike(on, marker ='^')
raster_plot_spike(off, marker = '*')
plt.show()
