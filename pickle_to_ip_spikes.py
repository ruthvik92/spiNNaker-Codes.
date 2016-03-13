'''this code converts the first time spike data(output) into usable input data assuming there is a pickle for output spikes'''
#########################################
# Author:Ruthvik Vaila, Boise State.    #
#                                       #
# License: Use as you like              #
#                                       #
#########################################
from random import randint
import pickle 
import random
b=pickle.load(open('afile','rb'))
spikes=[]
for c in range(int(b[-1][0])+1): ##this is number of neurons.
    spikes.append([])
print spikes

for i in range(int(b[-1][0])):  ##looping no.of neurons times
    for j in range(len(b)):   ##looping  to gather timings for each neuron
        if b[j][0]==i:
            spikes[i].append(int(b[j][1]))
        else:
            pass    ##passing, need not see other cases as elements are already
        #in order.

print len(spikes)

        
