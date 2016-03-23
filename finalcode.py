''' this code TRIES TO MAKE FULL SPIKE DATA  before running this code run poisson_pattern.py code to generate your pattern, 
remember to change the file name every time you generate new pattern because file name also changes, No.Of neurons should 
be same as the poisson_pattern.py code. Tries to Implement STDP based unsupervised learning.


k: because of biological issues the neurons fire a lil more time than specified time 'pattern_length' specified in other code.
pattern_gap: time after which pattern reappears again '''

Neurons=int(raw_input('Enter the total No.Of neurons in the simulation: '))
n= int(raw_input('Enter No of Patterns you totally want(n): '))
pattern_gap= int(raw_input('Enter the duration after which next pattern should appear(pattern_gap): '))
k=int(raw_input('Enter the extra time the i/p neurons spikes in pattern(usually pattern_duration+5 or 6 give 55 for now)(k): '))
weight_to_spike=1
import pyNN.spiNNaker as p
import pylab
import pickle
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep

# here the default parameters of the IF_curr_exp are used. These are:

# In PyNN, the neurons are declared in terms of a population of a number of neurons with similar properties
cell_params_lif = {'cm'        : 0.25, # nF #capacitance of LIF neuron in nF
                   'i_offset'  : 0.0,      #A base input current to add each timestep.(What current??)
                   'tau_m'     : 10.0,     #The time-constant of the RC circuit, in ms
                   'tau_refrac': 1.0,      #The refractory period in ms
                   'tau_syn_E' : 5.0,    #The excitatory input current decay time-constant
                   'tau_syn_I' : 5.0,    #The inhibitory input current decay time-constant
                   'v_reset'   : -70.0,  #The voltage to set the neuron at immediately after a spike
                   'v_rest'    : -65.0,  #The ambient rest voltage of the neuron
                   'v_thresh'  : -50.0    #The threshold voltage at which the neuron will spike.
                   }


## Load the 50ms_60Hz pickle poisson data

b=pickle.load(open('/home/ruthvik/Desktop/spikefile_800_50ms_60Hz','rb'))


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
project_stim_pop_ip_pop = p.Projection( stimlus_pop,ip_pop, p.OneToOneConnector(weights=10, delays=1.0), target="excitatory")

for i in range(1,n):
    IAddPre.append(p.Population(Neurons,
                                  p.SpikeSourcePoisson,
                                  {'rate': 50,
                                   'start': (k*i+pattern_gap*(i-1)),
                                   'duration': pattern_gap
                                   }))




for i in range(len(IAddPre)):
    p.Projection(IAddPre[i], ip_pop,p.OneToOneConnector(weights = 10.0,delays = 1.0),target = "excitatory")


t_rule = p.SpikePairRule (tau_plus=15, tau_minus=35, nearest=True) #The 2 parameters of this class identify the exponential decay rate of the STDP function(Curve)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=1.5, A_minus=7)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule) #STDP mechanism involving weight and timing.
s_d = p.SynapseDynamics(slow = stdp_model)#instantial of synaptic plasticity 


project_ip_op = p.Projection( ip_pop,op_pop, p.AllToAllConnector(weights=.475, delays=1.0), synapse_dynamics = s_d, target="excitatory")

stimlus_pop.record()
ip_pop.record()
op_pop.record()




p.run((pattern_gap+k)*n)


c=stimlus_pop.getSpikes()
v=ip_pop.getSpikes()
l=op_pop.getSpikes()

'''with open('/home/ruthvik/Desktop/file_'+str(Neurons)+'_'+str(n)+'patterns'+'_'+str(pattern_gap)+'ms'+str((pattern_gap+k)*n)+'totaltime', 'w') as f:   ##make a pickle of spike data
    pickle.dump(v,f)'''




spike_id = [i[0] for i in v]
spike_time = [i[1] for i in v]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, 0, Neurons])
pylab.show()


spike_id2 = [i[0] for i in l]
spike_time2 = [i[1] for i in l]
pylab.plot(spike_time2, spike_id2, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, -2, Neurons])
pylab.show()

weights = project_ip_op.getWeights()
print "final synaptic weight: ", weights

p.end()
