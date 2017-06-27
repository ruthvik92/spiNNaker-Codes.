import random
class weights():
    def __init__(self,window,number):
        self.window = window
        self.wam = [random.uniform(0,1) for i in range(0,window)]
    #def calcweights(self):
        #for i in range(0,self.window):
            #self.wam.append(random.uniform(0,1))
        #return self.wam
	

my_objects = [weights(3,i) for i in range(0,3)]


