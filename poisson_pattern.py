'''code was to generate poisson Xms pattern and pickle it and replot it to see if data is same

Hz: firing rate 
pattern_length: duration in ms of the pattern
Neurons: No of the input neurons.'''

Hz= int(raw_input('Enter the firing rate of the pattern: '))
pattern_length= int(raw_input('Enter the actual length(ms, give 50 for now) of the pattern: '))
Neurons=int(raw_input('Enter the total No.Of neurons in the simulation: '))
import pyNN.spiNNaker as p
import pylab
import pickle
p.setup(timestep = 1.0)  # runs using a 1.0ms timestep
n_neurons=800
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


stim_pop1 = p.Population(n_neurons, p.SpikeSourcePoisson,{"rate": Hz,"start":0, "duration":pattern_length } ) #Stimuluspopultn
ip_pop = p.Population(n_neurons, p.IF_curr_exp, cell_params_lif, label="inputneurons")


project_stim_pop_ip_pop = p.Projection( stim_pop1,ip_pop, p.OneToOneConnector(weights=10, delays=1.0), target="excitatory")

ip_pop.record()
stim_pop1.record()
p.run(70)
spikes4 = ip_pop.getSpikes()
spikes5=stim_pop1.getSpikes()

with open('/home/ruthvik/Desktop/spikefile_'+str(Neurons)+'_'+str(pattern_length)+'ms'+'_'+str(Hz)+'Hz','w') as f:   ##make a pickle of spike data
    pickle.dump(spikes4,f)


spike_time4 = [i[1] for i in spikes4]
spike_id4 = [i[0] for i in spikes4]
pylab.plot(spike_time4, spike_id4, ".")
pylab.xlabel("Time (ms)_stim_population")
pylab.ylabel("Neuron ID")
pylab.axis([0,70,0,Neurons])
pylab.show()

spike_time5 = [i[1] for i in spikes5]
spike_id5 = [i[0] for i in spikes5]
pylab.plot(spike_time5, spike_id5, ".")
pylab.xlabel("Time (ms)_input_population")
pylab.ylabel("Neuron ID")
pylab.axis([0,70,0,Neurons])
pylab.show()


b=pickle.load(open('/home/ruthvik/Desktop/spikefile_800_50ms_60Hz','rb')) ##see if pickled file is same as original file.

spike_time4 = [i[1] for i in b]
spike_id4 = [i[0] for i in b]
pylab.plot(spike_time4, spike_id4, ".")
pylab.xlabel("Time (ms)")
pylab.ylabel("Neuron ID")
pylab.axis([0,70,0,Neurons])
pylab.show()


##chahnge the pickle list format so that we can input the data as spike souce array.
spikes=[]                                                          ###
for c in range(int(b[-1][0])+1): ##this is number of neurons.
    spikes.append([])
#print spikes

for i in range(int(b[-1][0])):  ##looping no.of neurons times
    for j in range(len(b)):   ##looping  to gather timings for each neuron
        if b[j][0]==i:
            spikes[i].append(int(b[j][1]))
        else:
            pass    ##passing, need not see other cases as elements are already
        #in order.


        

p.end()

