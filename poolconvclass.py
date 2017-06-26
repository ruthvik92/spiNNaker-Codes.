
import math
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
class poolconv():
    
    '''    code tested for   |map     |window    |
                             |7       | 3 ov 1   |
                             |9       | 3 ov 1   |                         
                             |10      | 3 ov1 NW |
                             |10      | 3 ov 0   |
                        
            eg: here maps=5 means it's a 5x5 and window=2 means 2x2

                              - - - - - -
                              | | | | | | -
                              - - - - - -   -
                              | | | | | |     -
                              - - - - - -       -        - - - 
                              | | | | | |          }---> | | |
                              - - - - - -       -        - - -
                              | | | | | |     -          | | |
                              - - - - - -   -            - - -
                              | | | | | | - 
                              - - - - - -
  - -
  | | each of these boxes is a neuron, in this example we took window of 2x2 of neurons on leftside squares to form one 
  square on rightside squares. There is no overlap and one column on right and one row on bottom of leftside squares
  - -
   arguments are window, mapp, weight,delay,overlap
   The structure of list here is [pre_syn_neuron, post_syn_neuron, weight, axonal_delay]
    [(0, 0, 1, 1), (1, 0, 1, 1), (4, 0, 1, 1), (5, 0, 1, 1), (2, 1, 1, 1), (3, 1, 1, 1), (6, 1, 1, 1), (7, 1, 1, 1),
    (8, 2, 1, 1), (9, 2, 1, 1), (12, 2, 1, 1), (13, 2, 1, 1), (10, 3, 1, 1), (11, 3, 1, 1), (14, 3, 1, 1), (15, 3, 1, 1)]
This code can also be used for convolving populations. For performing convolution just enter the overlap value:
window-1'''
    conn_list = [(0,0,1,1)]
    def __init__(self,window,mapp,weight,delay,overlap):
        self.window = window
        self.mapp = mapp
        self.weight = weight
        self.delay = delay
        self.overlap = overlap
         	
    
    
    
    def PoolConv(self):
        
        ''' this method implements the logic for pooling/convolution. If overlap is window-1 then it's convolution.'''
        extra = int(math.floor((self.mapp-self.window)/(self.window-self.overlap)+1))
        
        for p in range(0,self.window-1):   
            w = self.conn_list[p][0]+1  
            v = self.conn_list[p][1]
            q = self.weight
            s = self.delay
            self.conn_list.append((w,v,q,s))


        for c in range(0,(self.window-1)*self.window):    
            x = self.conn_list[c][0] + self.mapp  
            y = self.conn_list[c][1]
            q = self.weight
            s = self.delay
            self.conn_list.append((x,y,q,s))

        skip = []
        for p in range(0,extra*extra):
            skip.append((p+1)*extra-1)    
        
                                                           
        for i in range(0,extra*extra-1):     
            if(i in skip):                 
                z = skip.index(i)
                for k in range(0+(self.window**2)*i,(self.window**2)+(self.window**2)*i):   
                    z = self.conn_list[(self.window**2)*skip[0]][0]
                    n = (self.conn_list[k][0] + self.mapp*(self.window-self.overlap)) -z   
                    m = self.conn_list[k][1] + 1  
                    q = self.weight
                    s = self.delay
                    new_item= (n,m,q,s)
                    self.conn_list.append(new_item)             

            else:
                for j in range(0+(self.window**2)*i,(self.window**2)+(self.window**2)*i):
                    a = self.conn_list[j][0] +self.window-self.overlap     
                    b = self.conn_list[j][1] +1
                    q = self.weight
                    s = self.delay
                    list1 = (a,b,q,s)
                    self.conn_list.append(list1)


    @staticmethod
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
            AllTs = AllTs.astype(float)/1000 - 5000.
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
            print 'file not existing'
            return [], []

    @staticmethod
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
        
            
           


    

        
                    

