''' This code implements(testing in progress) the STDP phenomenon like masqueliers STDP paper. This code requires spike data for that please run fullspikedata.py and
poisson_patter.py. This code also converts the spike_data from previous codes to format which can directly be given as input to spiNNaker, please change run time
and no of neurons according to your data sets'''

from random import randint
import random
import pickle
import pyNN.spiNNaker as p
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep
weight_to_spike=5
# here the default parameters of the IF_curr_exp are used. These are:

# In PyNN, the neurons are declared in terms of a population of a number of neurons with similar properties
cell_params_lif = {'cm'        : 0.25, # nF #capacitance of LIF neuron in nF
                   'i_offset'  : 0.0,      #A base input current to add each timestep.(What current??)
                   'tau_m'     : 2.0,     #The time-constant of the RC circuit, in ms
                   'tau_refrac': 2.0,      #The refractory period in ms
                   'tau_syn_E' : 5.0,    #The excitatory input current decay time-constant
                   'tau_syn_I' : 5.0,    #The inhibitory input current decay time-constant
                   'v_reset'   : -70.0,  #The voltage to set the neuron at immediately after a spike
                   'v_rest'    : -65.0,  #The ambient rest voltage of the neuron
                   'v_thresh'  : -50.0    #The threshold voltage at which the neuron will spike.
                   }

b=pickle.load(open('/home/ruthvik/Desktop/file_700_100patterns_100ms15500totaltime','rb'))


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

with open('/home/ruthvik/Desktop/ip_spikes_file_700_100patterns_100ms15500totaltime', 'w') as f:   ##make a pickle of spike data
    pickle.dump(spikes,f)


input = p.Population(800,p.IF_curr_exp, cell_params_lif,label="pop_1")

stim_pop_pattern = p.Population(800, p.SpikeSourceArray, {'spike_times': spikes})

op_pop = p.Population(1, p.IF_curr_exp, cell_params_lif, label='outputneuron')


p.Projection(stim_pop_pattern, input,p.OneToOneConnector(weights = 10.0,delays = 0),target = "excitatory")
##setting up the parameters for STDP
t_rule = p.SpikePairRule (tau_plus=16.8, tau_minus=33.7) #The 2 parameters of this class identify the exponential decay rate of the STDP function(Curve)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=0.03125, A_minus=0.85*A_plus)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule) #STDP mechanism involving weight and timing.
s_d = p.SynapseDynamics(slow = stdp_model)#instantial of synaptic plasticity 


project_ip_op = p.Projection( input,op_pop, p.AllToAllConnector(weights=.475, delays=0), synapse_dynamics = s_d, target="excitatory")

input.record()
op_pop.record()
input.record_v()
p.run(15500)


import pylab
v = input.getSpikes()
spikes1 = input.getSpikes()
spikes2 = op_pop.getSpikes()
weights = project_ip_op.getWeights()
print "final synaptic weight: ", weights


spike_time = [i[1] for i in spikes1]
spike_id = [i[0] for i in spikes1]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, 15500, 0, 700])
pylab.show()


spikes2 = op_pop.getSpikes()
spike_time2 = [i[1] for i in spikes2]
spike_id2 = [i[0] for i in spikes2]
pylab.plot(spike_time2, spike_id2, ".")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([-2,15500,-2, 1])
pylab.show()
