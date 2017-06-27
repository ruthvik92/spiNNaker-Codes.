import random
class weights():    
    '''Returns a list whose items are objects of weights between a windowxwindow neurons and a neuron in next map.
       Call the returnobjs function.
    '''
       
    def __init__(self,window,number):
        self._window = window
        self.wam = [random.uniform(0,1) for i in range(0,self._window*self._window)]
        
    @staticmethod
    def returnobjs(window,i):
        

        
        '''
           :param window: Size of the window
           :param number: Number of maps in the next step
        '''
           
        window = window
        j = i
        return [weights(window,i) for i in range(0,j)]
        
	


##### Example of pass by reference
def afunc(a):
    a.wam[0]=a.wam[0]+1
    




c = weights.returnobjs(3,3)

print c[0].wam

afunc(c[0])

print c[0].wam


