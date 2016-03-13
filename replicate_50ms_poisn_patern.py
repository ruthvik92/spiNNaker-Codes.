''' this code replicates 50m spike pattern over specified no of times for particular duration'''




import pyNN.spiNNaker as p
import pylab
import pickle
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep
n_neurons=800
n= int(raw_input('Enter No of Patterns+1 you totally want: '))
pattern_gap= int(raw_input('Enter the duration after which next pattern should appear: '))

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


## Load the 50ms_60Hz pickle poisson data

b=pickle.load(open('/home/ruthvik/Desktop/spikefile_800_50ms','rb'))


'''spike_time = [i[1] for i in b]
spike_id = [i[0] for i in b]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, 50, 0, 800])
pylab.show()'''


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
           spikes[i].append((pattern_gap)*c+spikes[i][j])



##input the replicated data to spinnaker.
stimlus_pop = p.Population(800, p.SpikeSourceArray, {'spike_times': spikes})
ip_pop = p.Population(800, p.IF_curr_exp, cell_params_lif, label="inputneurons")

project_stim_pop_ip_pop = p.Projection( stimlus_pop,ip_pop, p.OneToOneConnector(weights=10, delays=0.0), target="excitatory")

stimlus_pop.record()

p.run(pattern_gap*n)
v=stimlus_pop.getSpikes()

spike_time = [i[1] for i in v]
spike_id = [i[0] for i in v]
pylab.plot(spike_time, spike_id, ".")
pylab.xlabel("Time(ms)")
pylab.ylabel("NeuronID")
pylab.axis([0, pattern_gap*n, 0, 800])
pylab.show()
p.end()
