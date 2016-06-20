''' 
There are 700 input neurons and 1 output neuron and there is one to one connection between them. A pattern hidden in random poisson spiking is given as an input to 700 neurons,
after sometime the output neuron only fires when there is pattern and it remains silent for random(stochastic) input spikes.
 Before running this code, ensure you have pickle file for the pattern, remember to change the path to supplied pickle file(pattern) 

Use the supplied pickle file.

No.Of neurons should be same as in pickle file(here it is 700)

Firing rate should same as in pickle file(here it is 6Hz).


k: this is the length of the pattern(here it is 50ms) 
pattern_gap: time after which pattern reappears again, say 200 or 150 '''

Neurons=int(raw_input('Enter the total No.Of neurons in the simulation, here it is 700 as in supplied pickled pattern file)
n= int(raw_input('Enter No of Patterns you totally want(n), say 100 or 200 or 250 : '))
pattern_gap= int(raw_input('Enter the duration after which next pattern should appear(pattern_gap)say, 150 or 200: '))
k=int(raw_input('Enter the extra time the i/p neurons spikes in pattern(give 50 for now)(k): '))
weight_to_spike=1.0
import pyNN.spiNNaker as p
import pylab
import pickle
import numpy as np
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


t_rule = p.SpikePairRule (tau_plus=16.8, tau_minus=33.7) #The 2 parameters of this class identify the exponential decay rate of the STDP function(Curve)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=0.03125, A_minus=0.85*0.03125)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule) #STDP mechanism involving weight and timing.
s_d = p.SynapseDynamics(slow = stdp_model)#instantial of synaptic plasticity 


#weights=np.random.uniform(0.1,0.48,50)
#print weights
#weights=RandomDistribution(distribution='iniform',parameters=[0.1,0.475])
#weights=p.RandomDistribution(distribution='uniform',parameters=[2,5])
#print weights
project_ip_op = p.Projection( ip_pop,op_pop, p.AllToAllConnector(weights=.475, delays=1), synapse_dynamics = s_d, target="excitatory")
##weights1 = project_ip_op.getWeights()
##print "final Synaptic Weights",weights1
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



print "output pop example spikes", l[0],l[1],l[2],l[3],l[4],l[5]
spike_id2 = [i[0] for i in l]
spike_time2 = [i[1] for i in l]
#***pylab.subplot(3,1,2)
pylab.plot(spike_time2, spike_id2, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, -2, Neurons])
pylab.show()



weights = project_ip_op.getWeights()
print "final synaptic weight: ", weights##


volts=[]
print "voltage eg values",vo[0],vo[1],vo[2],vo[3],vo[4],vo[4],vo[7],vo[8],vo[10],vo[15],vo[15],vo[20],vo[25],vo[100],vo[100],vo[1000],vo[1001]
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


#cell_params_lif = {'cm'        : 0.35, # nF #capacitance of LIF neuron in nF
 #                  'i_offset'  : 0.0,      #A base input current to add each timestep.(What current??)
  #                 'tau_m'     :25,     #The time-constant of the RC circuit, in ms
   #                'tau_refrac': 7,      #The refractory period in ms
    #               'tau_syn_E' : 5,    #The excitatory input current decay time-constant
     #              'tau_syn_I' : 5,    #The inhibitory input current decay time-constant
      #             'v_reset'   : -70.6,  #The voltage to set the neuron at immediately after a spike
       #            'v_rest'    : -65,  #The ambient rest voltage of the neuron
        ##          }
