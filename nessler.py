'''' THIS CODE TRIES TO IMPLEMENT THE LAST APPLICATION FROM NESSLER'S STDP-EM PAPER'''
Neurons=int(raw_input('Enter the total No.Of neurons(700) in the simulation: '))
n= int(raw_input('Enter No of Patterns you totally want(n): '))
pattern_gap= int(raw_input('Enter the duration after which next pattern should appear(pattern_gap) 250: '))
k=int(raw_input('Enter the pattern length, for now give 50)(k): '))
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
                   'tau_syn_I' : 10,    #The inhibitory input current decay time-constant
                   'v_reset'   : -70.6,  #The voltage to set the neuron at immediately after a spike
                   'v_rest'    : -65,  #The ambient rest voltage of the neuron
                   'v_thresh'  : -50.  #The threshold voltage at which the neuron will spike.
                   }




################################################%%%%%%%%%%%%CONSTRUCTING THE PATTERN%%%%%%%%%%%############%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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



#print '**************************',spikes

b1=pickle.load(open('/home/ruthvik/Desktop/spikefile2_700_50ms_6Hz','rb'))
spikes1=[]
### change the pickle file spike data format so that it can be given poisson spike source

for c in range(int(b1[-1][0])+1): ##this is number of neurons.
    spikes1.append([])
for i in range(int(b1[-1][0])):  ##looping no.of neurons times
    for j in range(len(b1)):   ##looping  to gather timings for each neuron
        if b1[j][0]==i:
            spikes1[i].append(int(b1[j][1]))
        else:
            pass    ##passing, need not see other cases as elements are already
        #in order.


## replicate the 50ms previous poisson spike data n number of times.


spikes1.append([])

print "length of spikes1",len(spikes1) 
print "length of spikes",len(spikes)
q=[]
for i in range(len(spikes)):
    q.append([])
for i in range(len(spikes)):    
    for c in range(0,n):
          if c%2 ==0:
              #print c
              for j in range(len(spikes[i])):
                  q[i].append((pattern_gap+k)*c+spikes[i][j])

          else:
              for j in range(len(spikes1[i])):
                  q[i].append((pattern_gap+k)*c+spikes1[i][j])


##################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%$#############$$$%^^END OF PATTERN CONSTRUCTION##############$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                           ##################################################
                                                 ####################################
                                                           ################

##########%%%%%%%%%%%%$$$$$$$$$$$$$$$$DECLARING THE POPULATIONS AND PROJECTIONS#############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

###STIMULUS POPULATION FOR INPUT NEURONS
stimlus_pop = p.Population(Neurons,p.SpikeSourceArray, {'spike_times': q})

###INPUT OPULATION DECLARATION
ip_pop = p.Population(Neurons, p.IF_curr_exp, cell_params_lif, label="inputneurons")

####OUTPUT POPULATIOn DECLARATION
op_pop = p.Population(3, p.IF_curr_exp, cell_params_lif, label='outputneuron')


#####INHIBITORY POPULATION NEAR OUTPUT NEURONS
pop_inh = p.Population(3, p.IF_curr_exp, cell_params_lif,label="Inhibitory")


#####PROJECTING STIMULUS POP ONTO IP_POP WITH EXCITATORY SYNAPSES
project_stim_pop_ip_pop = p.Projection( stimlus_pop,ip_pop, p.OneToOneConnector(weights=10, delays=1), target="excitatory")



#####RANDOM WEIGHTS IN BETWEEN IP_POP AND OP_POP
weights=p.RandomDistribution(distribution='uniform',parameters=[0.1,0.475])




#PROJECTING IP_POP ONTO POP_INH WITH EXCITATORY SYNAPSES
project_op_inh = p.Projection(op_pop,pop_inh, p.AllToAllConnector(weights=5, delays=1), target="excitatory")

###PROJECTING POP_INH ONTO IP_POP   WITH INHIBITORY  SYNAPSES
project_inh_op = p.Projection(pop_inh, op_pop, p.AllToAllConnector(weights=5, delays=1), target="inhibitory")

######################$$$$$$$$$$$$$$%%%%%%%%%%%%END OF POPULATION AND PROJECTION DECLARATION#############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                                            ##################################################
                                                 ####################################
                                                           ################
#####################$$$$$$$$$$$$$$$%%%%%%%%%%%%%%CONSTRUCT THE NOISE ################################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
IAddPre = []
for i in range(1,n):
    IAddPre.append(p.Population(Neurons,
                                  p.SpikeSourcePoisson,
                                  {'rate': 6,
                                   'start': (k*i+pattern_gap*(i-1)),
                                   'duration': pattern_gap
                                   }))




for i in range(len(IAddPre)):
    p.Projection(IAddPre[i], ip_pop,p.OneToOneConnector(weights = 10.0,delays = 1.0),target = "excitatory")
#####################$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%% END OF NOISE CONSTRUCTION#############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                                            ##################################################
                                                 ####################################
                                                           ################
##############################$$$$$$$$$$$$$$$$$STDP MECHANISM#########################$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t_rule = p.SpikePairRule (tau_plus=16.8, tau_minus=33.7) #The 2 parameters of this class identify the exponential decay rate of the STDP function(Curve)
w_rule = p.AdditiveWeightDependence (w_min=0.0, w_max=weight_to_spike, A_plus=0.03125, A_minus=0.85*0.03125)
stdp_model = p.STDPMechanism (timing_dependence = t_rule, weight_dependence = w_rule) #STDP mechanism involving weight and timing.
s_d = p.SynapseDynamics(slow = stdp_model)#instantial of synaptic plasticity 


##PROJECTING IP_POP ONTO OP_POP WITH STDP DYNAMIC SYNAPSES
project_ip_op = p.Projection( ip_pop,op_pop, p.AllToAllConnector(weights=weights, delays=1), synapse_dynamics = s_d, target="excitatory")

########################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$END OF STDPMechanism ####################################################################
                                           ##################################################
                                                 ####################################
                                                           ################
##############################################$$$$$$$$$$$$$$$$$$$$PLOTTING AND RECORDING #######################################################
stimlus_pop.record()
ip_pop.record()
op_pop.record()
op_pop.record_v()

p.run((pattern_gap+k)*n)


c=stimlus_pop.getSpikes()
v=ip_pop.getSpikes()
l=op_pop.getSpikes()
vo=op_pop.get_v()

print "Output Population voltage", vo
print "Output Population voltage", vo[1]

spike_id = [i[0] for i in v]
spike_time = [i[1] for i in v]
#***pylab.subplot(3,1,1)
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, (pattern_gap+k)*n, 0, Neurons])
pylab.show()




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
