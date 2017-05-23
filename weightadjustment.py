

# This code needs the final weights from the stdmasq.py. It nullifies the weights which are not significant (less than 0.5) and runs the simulation. It gives 100% accuracy.  
Neurons=int(raw_input('Enter the total No.Of neurons in the simulation, here it is 700 as in supplied pickled pattern file:'))
n= int(raw_input('Enter No of Patterns you totally want(n), say 100 or 200 or 250 : '))
pattern_gap= int(raw_input('Enter the duration after which next pattern should appear(pattern_gap)say, 150 or 200: '))
k=int(raw_input('Enter the extra time the i/p neurons spikes in pattern(give 50 for now)(k): '))
weight_to_spike=1.0
import pyNN.spiNNaker as p
import pylab
import pickle
import numpy as np
import matplotlib.pyplot as plt
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep

# here the default parameters of the IF_curr_exp are used. These are:

# In PyNN, the neurons are declared in terms of a population of a number of neurons with similar properties
cell_params_lif = {'cm'        : 0.35, # nF #capacitance of LIF neuron in nF
                   'i_offset'  : 0.0,      #A base input current to add each timestep.(What current??)
                   'tau_m'     : 4,     #The time-constant of the RC circuit, in ms
                   'tau_refrac': 1,      #The refractory period in ms
                   'tau_syn_E' : 1,    #The excitatory input current decay time-constant
                   'tau_syn_I' : 5,    #The inhibitory input current decay time-constant
                   'v_reset'   : -70.6,  #The voltage to set the neuron at immediately after a spike
                   'v_rest'    : -65,  #The ambient rest voltage of the neuron
                   'v_thresh'  : -50.  #The threshold voltage at which the neuron will spike.
                   }


## Load the 50ms_60Hz pickle poisson data

b=pickle.load(open('/home/ruthvik/Desktop/spikefile_700_50ms_6Hz','rb'))


spikes=[]
### change the pickle file spike data format so that it can be given poisson spike source

for c in range(int(b[-1][0])+1): ##this is number of neurons.
    spikes.append([])
for i in range(int(b[-1][0])):  ##looping no.of neurons times
    for j in range(len(b)):   ##looping  to gather timings for each neuron
        if b[j][0]==i:
            spikes[i].append(int(b[j][1]))
        else:
            pass    ##passing, need not see other cases as elements are already
        #in order.


## replicate the 50ms previous poisson spike data n number of times.

for i in range(len(spikes)):                                   ##Here we are replicating the pattern. 
      for j in range(len(spikes[i])):
         for c in range(1,n):
           spikes[i].append((pattern_gap+k)*c+spikes[i][j])


IAddPre = []
           


##input the replicated data to spinnaker.
stimlus_pop = p.Population(Neurons,p.SpikeSourceArray, {'spike_times': spikes})

ip_pop = p.Population(Neurons, p.IF_curr_exp, cell_params_lif, label="inputneurons")
op_pop = p.Population(1, p.IF_curr_exp, cell_params_lif, label='outputneuron')
project_stim_pop_ip_pop = p.Projection( stimlus_pop,ip_pop, p.OneToOneConnector(weights=10, delays=1), target="excitatory")

###make noise i.e creating stochastic spike data

for i in range(1,n):
    IAddPre.append(p.Population(Neurons,
                                  p.SpikeSourcePoisson,
                                  {'rate': 6,
                                   'start': (k*i+pattern_gap*(i-1)),
                                   'duration': pattern_gap
                                   }))




for i in range(len(IAddPre)):
    p.Projection(IAddPre[i], ip_pop,p.OneToOneConnector(weights = 10.0,delays = 1.0),target = "excitatory")



c = [0.14453125, 0.8203125, 0.33203125, 0.0, 0.3671875, 0.2421875, 0.109375, 0.41796875, 0.21484375, 0.18359375, 0.1640625, 0.140625, 0.21484375, 0.0, 0.04296875, 0.7578125, 0.3515625, 0.0, 0.34765625, 1.0, 0.0, 0.09765625, 0.1171875, 0.171875, 0.16015625, 0.16796875, 0.1015625, 0.140625, 0.3671875, 0.0625, 0.375, 0.109375, 0.04296875, 0.0, 0.03515625, 0.2890625, 0.1640625, 0.2109375, 0.140625, 0.20703125, 0.26171875, 0.22265625, 0.0625, 0.0, 0.171875, 0.73828125, 0.140625, 0.28515625, 0.0, 0.21875, 0.1015625, 0.1484375, 0.00390625, 0.33203125, 0.0078125, 0.12109375, 0.0, 0.21484375, 0.171875, 0.00390625, 0.21484375, 0.265625, 0.0, 0.4609375, 0.0, 0.171875, 0.01953125, 0.578125, 0.15234375, 0.24609375, 0.00390625, 0.19140625, 0.54296875, 0.2265625, 0.3203125, 0.1171875, 0.42578125, 0.30859375, 0.0, 0.51171875, 0.3203125, 0.24609375, 0.4921875, 0.3515625, 0.625, 0.2890625, 0.0, 0.44140625, 0.31640625, 0.08984375, 0.35546875, 0.0, 0.0, 0.0703125, 0.0, 0.17578125, 0.41796875, 0.44921875, 0.7265625, 0.08984375, 0.3515625, 0.2734375, 0.390625, 0.1015625, 0.02734375, 0.48046875, 0.20703125, 0.2421875, 0.73828125, 0.0, 0.15234375, 0.0, 0.0, 0.2421875, 0.19140625, 0.078125, 0.78515625, 0.04296875, 0.13671875, 0.1015625, 0.0, 0.26953125, 0.97265625, 0.0, 0.53125, 0.0, 0.02734375, 0.2109375, 0.08203125, 0.09765625, 0.0, 0.23046875, 0.0625, 0.16796875, 0.0, 0.140625, 0.0, 0.00390625, 0.10546875, 0.26171875, 0.29296875, 0.4375, 0.125, 0.23046875, 0.44140625, 0.34375, 0.11328125, 0.421875, 0.0, 0.39453125, 0.375, 0.32421875, 0.109375, 0.46484375, 0.0, 0.0234375, 0.05078125, 0.0, 0.2734375, 0.0, 0.1171875, 0.05078125, 0.4140625, 0.0, 0.33203125, 0.0, 0.17578125, 1.0, 0.62890625, 0.171875, 0.18359375, 0.046875, 0.09765625, 0.11328125, 0.0390625, 0.05859375, 0.17578125, 0.0, 0.1796875, 0.33203125, 0.3125, 0.0, 0.26953125, 0.0, 0.48828125, 0.03515625, 0.15234375, 0.23046875, 0.07421875, 0.0, 0.3515625, 0.0234375, 0.140625, 0.0, 0.453125, 0.0, 0.0, 0.6953125, 1.0, 0.40625, 0.12109375, 0.48828125, 0.296875, 0.35546875, 0.0703125, 0.55859375, 0.2421875, 0.0, 0.1796875, 0.2109375, 0.125, 0.0, 0.3671875, 0.0, 0.0, 0.62109375, 0.0, 0.44921875, 0.05859375, 0.046875, 0.3203125, 0.1015625, 1.0, 0.0390625, 0.296875, 0.1875, 0.203125, 0.453125, 0.14453125, 0.0, 0.0234375, 0.15234375, 0.4375, 0.0, 0.0, 0.0, 0.0, 0.1484375, 0.046875, 0.21875, 0.296875, 0.02734375, 0.0625, 0.02734375, 0.0, 0.29296875, 0.37109375, 0.0, 0.265625, 0.0078125, 0.33203125, 1.0, 0.0, 0.44921875, 0.0, 0.015625, 0.03515625, 0.04296875, 0.24609375, 0.0234375, 0.078125, 0.234375, 0.20703125, 0.21484375, 0.296875, 0.171875, 0.03125, 0.31640625, 0.55859375, 0.234375, 0.0, 0.2578125, 0.109375, 0.2578125, 0.91015625, 0.078125, 0.53125, 0.11328125, 0.0, 0.1640625, 0.26171875, 0.02734375, 0.0, 0.06640625, 0.03125, 0.65625, 0.0234375, 0.04296875, 0.0, 0.07421875, 0.13671875, 0.19140625, 0.53515625, 0.01953125, 0.0, 0.1640625, 0.0078125, 0.14453125, 0.0, 0.50390625, 0.0703125, 0.16796875, 0.0, 0.5859375, 0.75390625, 0.0234375, 0.0, 0.08203125, 0.296875, 0.0, 0.06640625, 0.0, 0.1953125, 0.3359375, 0.01171875, 0.41796875, 0.00390625, 1.0, 0.5625, 0.0, 0.0, 0.3359375, 0.4921875, 0.00390625, 0.13671875, 0.05859375, 0.1640625, 0.03515625, 0.0, 0.59375, 0.296875, 0.48046875, 0.4609375, 0.2421875, 0.09765625, 0.2578125, 0.0390625, 0.0, 0.15625, 0.36328125, 0.0, 0.0, 0.7265625, 0.15234375, 0.08984375, 0.40234375, 0.04296875, 0.0, 0.0, 0.296875, 0.08203125, 0.08984375, 0.265625, 0.2421875, 0.1171875, 0.04296875, 0.04296875, 0.1328125, 0.234375, 0.38671875, 0.078125, 1.0, 0.265625, 0.1875, 0.1796875, 0.375, 0.0, 0.0234375, 0.0, 0.0625, 0.1015625, 0.015625, 0.1875, 0.0, 0.0, 0.6796875, 0.5234375, 0.0, 0.0, 0.078125, 0.13671875, 0.9453125, 0.0, 0.03515625, 0.0, 0.32421875, 0.32421875, 0.0, 0.0, 0.47265625, 0.34765625, 0.37109375, 0.0, 0.296875, 0.33203125, 0.33203125, 0.60546875, 0.26171875, 0.1484375, 0.41015625, 0.34765625, 0.0, 0.17578125, 0.23828125, 0.0546875, 0.0, 0.0, 0.0, 0.890625, 0.0390625, 0.0, 0.1953125, 0.58203125, 0.0, 0.0703125, 0.38671875, 0.03515625, 0.30859375, 0.0078125, 0.27734375, 0.0, 0.64453125, 0.76171875, 0.1484375, 0.0, 0.19921875, 0.203125, 0.26171875, 0.11328125, 0.03125, 0.42578125, 0.26953125, 0.67578125, 0.0, 0.3671875, 0.32421875, 0.0, 0.0, 0.078125, 0.0, 0.1875, 0.49609375, 0.4609375, 0.0, 0.0, 0.0, 0.26953125, 0.19921875, 0.25, 0.3203125, 0.0390625, 0.546875, 0.0, 0.0390625, 0.96484375, 0.0, 0.09765625, 0.0, 0.0, 0.05078125, 0.0, 0.33203125, 0.2734375, 0.1796875, 0.0, 0.0078125, 0.0, 0.1015625, 0.42578125, 0.23046875, 0.0, 0.0078125, 0.0, 0.0703125, 0.0546875, 0.72265625, 0.33203125, 0.0, 0.33203125, 0.0390625, 0.96484375, 0.0859375, 0.02734375, 0.0, 0.0, 0.44921875, 0.1796875, 0.1171875, 0.0, 0.0, 0.0, 0.984375, 0.87890625, 0.00390625, 0.22265625, 0.36328125, 0.05859375, 0.14453125, 0.296875, 0.0, 0.85546875, 0.15234375, 0.34375, 0.015625, 0.3203125, 0.1953125, 0.16796875, 0.35546875, 0.0, 0.4765625, 0.0, 0.26953125, 1.0, 0.0, 0.69140625, 0.1796875, 0.0, 0.32421875, 0.046875, 0.38671875, 0.0, 0.3984375, 0.25390625, 0.0, 0.0, 0.0, 0.29296875, 0.4453125, 0.23828125, 0.97265625, 0.14453125, 0.125, 0.14453125, 0.0, 0.0, 0.515625, 0.23828125, 0.359375, 0.0, 0.0, 0.01171875, 0.2109375, 0.2890625, 0.06640625, 0.3515625, 0.3671875, 0.0, 0.078125, 0.359375, 0.0, 0.1640625, 0.23828125, 0.0, 0.0, 0.11328125, 0.3515625, 0.3359375, 0.16015625, 0.50390625, 0.140625, 0.0, 0.0, 0.23828125, 0.0625, 0.1328125, 0.25, 0.0, 0.0, 0.0, 0.0, 0.07421875, 0.0, 0.2109375, 0.25390625, 0.0, 0.0, 0.0, 0.109375, 0.26171875, 0.04296875, 0.8046875, 0.14453125, 0.515625, 0.046875, 0.0, 0.2578125, 0.09375, 0.21875, 0.17578125, 0.0, 0.3359375, 0.0, 0.0078125, 0.14453125, 0.0, 0.16796875, 0.16015625, 0.50390625, 0.12890625, 0.125, 0.109375, 0.8125, 0.25390625, 0.08984375, 0.0, 0.56640625, 0.4765625, 0.16796875, 0.265625, 0.10546875, 0.140625, 0.17578125, 0.4921875, 0.0, 0.0, 0.171875, 0.4375, 0.14453125, 0.39453125, 0.26953125, 0.41796875, 0.78125, 0.12890625, 0.0, 0.0, 0.02734375, 0.0, 0.0703125, 0.2265625, 0.19140625, 0.0, 0.37890625, 0.140625, 0.50390625, 0.62890625, 0.0078125, 0.0, 0.07421875, 0.37109375, 0.29296875, 0.4765625, 0.046875, 0.12890625, 0.046875, 0.12890625, 0.26171875, 0.01171875, 0.20703125, 0.01171875, 0.33984375, 0.44140625, 0.30859375, 0.3125, 0.015625, 0.26953125, 0.078125, 0.31640625, 0.18359375, 0.26953125, 0.1875, 0.0, 0.3984375, 0.0, 0.04296875, 0.25390625, 0.2734375, 0.01953125, 0.078125, 0.015625, 0.0, 0.1875, 0.0, 0.5703125, 0.078125, 0.0, 0.02734375, 1.0, 0.15625, 0.00390625, 0.33984375, 0.125, 0.24609375, 0.44921875, 1.0, 0.0078125, 0.0, 0.24609375, 0.20703125, 0.01171875, 0.12890625, 0.44140625, 0.0234375, 0.01953125, 0.3515625, 0.09375, 0.4296875, 0.08203125, 0.26171875, 0.01953125, 0.296875]

for i in range(0,len(c)):
    if c[i] <= 0.5:
        c[i]= 0

weights = c

conn_list = []
for i in range(0, Neurons):
    conn_list.append((i, 0, weights[i], 1))

project_ip_op = p.Projection( ip_pop,op_pop, p.FromListConnector(conn_list), target="excitatory")
weights1 = project_ip_op.getWeights()
print "final Synaptic Weights",weights1
stimlus_pop.record()
ip_pop.record()
op_pop.record()
op_pop.record_v()

p.run((pattern_gap+k)*n)


c=stimlus_pop.getSpikes()
v=ip_pop.getSpikes()
l=op_pop.getSpikes()
vo=op_pop.get_v()

#with open('/home/ruthvik/Desktop/file_'+str(Neurons)+'_'+str(n)+'patterns'+'_'+str(pattern_gap)+'ms'+str((pattern_gap+k)*n)+'totaltime', 'w') as f:   ##make a pickle of spike data
 #   pickle.dump(c,f)




spike_id = [i[0] for i in v]
spike_time = [i[1] for i in v]
#***pylab.subplot(3,1,1)
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, 0, Neurons])
pylab.show()


#print "input spikes", v[0:20]
#print spike_id
#print spike_time 
#spike_id_split = spike_id[0:(pattern_gap+k)*n:250]




#print "output pop example spikes", l[0:20]
spike_id2 = [i[0] for i in l]
spike_time2 = [i[1] for i in l]
#***pylab.subplot(3,1,2)
pylab.plot(spike_time2, spike_id2, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, -2, Neurons])
pylab.show()



weights = project_ip_op.getWeights()
#print "final synaptic weight: ", weights##
#d = list(range(700))
#plt.scatter(weights,d, marker = "+")
#plt.show()

imp_spike_time_index = []
imp_spike_time = []

for r in range(len(spike_time)):
    if spike_time[r]<=5:
        imp_spike_time_index.append(r)
        imp_spike_time.append(spike_time[r])  

#print "imp_spike-time", imp_spike_time
#print "imp_spike-time_index", imp_spike_time_index


imp_spike_id = []

for j in range(len(imp_spike_time)):
    imp_spike_id.append(spike_id[imp_spike_time_index[j]])

#print "imp_spike-id", imp_spike_id

fig, ax = plt.subplots()
ax.scatter(spike_time, spike_id, marker = "+")
ax.scatter(imp_spike_time, imp_spike_id, marker = "+")

for i, txt in enumerate(imp_spike_id):
    ax.annotate(txt, (imp_spike_time[i]+0.01, imp_spike_id[i]+0.01))
    ax.annotate('Pattern', xy=(275,200), xytext=(150,400),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('Pattern', xy=(25,200), xytext=(150,400),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate('Neurons involved in the initial 5ms of the pattern', xy=(5,400), xytext=(50,600),
                arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlabel('Time(ms)', fontsize=18)
plt.ylabel('Neuron ID No.', fontsize=18)
plt.axvspan(0,50, color='red', alpha=0.5)
plt.axvspan(250,300, color='red', alpha=0.5)
plt.show()


volts=[]
for i in range(0,(pattern_gap+k)*n):
    volts.append(vo[i][2])

time=[]
for i in range(0,(pattern_gap+k)*n):
    time.append(vo[i][1])

#***pylab.subplot(3,1,3)
pylab.plot(time,volts , "-")
pylab.xlabel("Time (ms)")
pylab.ylabel("Volts (mv)")
pylab.axis([0, (pattern_gap+k)*n, -110, -40])

pylab.show()



   

p.end()
