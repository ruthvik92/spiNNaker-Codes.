""" 
There are 700 Input Neurons and 1 output neuron and the there is OneToOneConnection between them. SynapseDynamics are based on STDPMechanism 
 The input spikedata is an already constructed pickle file.
"""
weight_to_spike=1
import pyNN.spiNNaker as p
import pylab
import pickle
import numpy as np
Neurons=700
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep

# here the default parameters of the IF_curr_exp are used. These are:

# In PyNN, the neurons are declared in terms of a population of a number of neurons with similar properties
cell_params_lif = {'cm'        : 0.281, # nF #capacitance of LIF neuron in nF
                   'i_offset'  : 0.0,      #A base input current to add each timestep.(What current??)
                   'tau_m'     : 20,     #The time-constant of the RC circuit, in ms
                   'tau_refrac': 15,      #The refractory period in ms
                   'tau_syn_E' : 2.5,    #The excitatory input current decay time-constant
                   'tau_syn_I' : 20.0,    #The inhibitory input current decay time-constant
                   'v_reset'   : -70.6,  #The voltage to set the neuron at immediately after a spike
                   'v_rest'    : -70.6,  #The ambient rest voltage of the neuron
                   'v_thresh'  : -50.4    #The threshold voltage at which the neuron will spike.
                   }

###These are spikes for neurons from 350-699####################
spikes=pickle.load(open('/home/ruthvik/Desktop/Ready Test Cases/TestCase_50ms_20Hz/spikefile_350_50000ms_20HzReady','rb'))
###########These are spikes for Neurons for 0-349 neurons###############################################
spikes1=pickle.load(open('/home/ruthvik/Desktop/Ready Test Cases/TestCase_50ms_20Hz/spikefile_350_50ms_20HzLowerSpikesReady','rb'))

#######combining the upper 350 and lower 350 spikes###########################
for i in range(0,350):
	spikes[i]=spikes1[i]


#######Defining Input,Stimulus,Output Populations.#####################
stimlus_pop = p.Population(700,p.SpikeSourceArray, {'spike_times': spikes})
ip_pop = p.Population(700, p.IF_curr_exp, cell_params_lif, label="inputneurons")
project_stim_pop_ip_pop = p.Projection( stimlus_pop,ip_pop, p.OneToOneConnector(weights=10, delays=1), target="excitatory")
op_pop = p.Population(1, p.IF_curr_exp, cell_params_lif, label='outputneuron')

################Defining the STDP RULE##################################
t_rule = p.SpikePairRule (tau_plus=16.8, tau_minus=33.7,nearest=True) #The 2 parameters of this class identify the exponential decay rate of the STDP function(Curve) #(#70,60,40,20)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=0.01, A_minus=0.01)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule) #STDP mechanism involving weight and timing.
s_d = p.SynapseDynamics(slow = stdp_model)#instantial of synaptic plasticity 


##################Making connections#######################################
project_ip_op = p.Projection( ip_pop,op_pop, p.AllToAllConnector(weights=0.475 , delays=1), synapse_dynamics = s_d, target="excitatory")

############################Recording the spikes from populations######################
ip_pop.record()

p.run(50000)

stimlus_pop.record()
ip_pop.record()
op_pop.record()
op_pop.record_v()

v=ip_pop.getSpikes()
l=op_pop.getSpikes()
vo=op_pop.get_v()


spike_id = [i[0] for i in v]
spike_time = [i[1] for i in v]
pylab.subplot(3,1,1)
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, 50000, 0, Neurons])




spike_id2 = [i[0] for i in l]
spike_time2 = [i[1] for i in l]
pylab.subplot(3,1,2)
pylab.plot(spike_time2, spike_id2, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, 50000, -2, Neurons])



weights = project_ip_op.getWeights()
print "final synaptic weight: ", weights##


volts=[]
for i in range(0,50000):
    volts.append(vo[i][2])

time=[]
for i in range(0,50000):
    time.append(vo[i][1])

pylab.subplot(3,1,3)
pylab.plot(time,volts , "-")
pylab.xlabel("Time (ms)")
pylab.ylabel("Volts (mv)")
pylab.axis([0, 50000, -110, -40])

pylab.show()
