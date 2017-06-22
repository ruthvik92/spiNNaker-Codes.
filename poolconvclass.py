
import math    
class poolconv():
    '''    code tested for   |map     |window    |
                             |7       | 3 ov 1   |
                             |9       | 3 ov 1   |                         
                             |10      | 3 ov1 NW |
                             |10      | 3 ov 0   |
                        
            eg: here maps=5 means it's a 5x5 and window=2 means 2x2

                              - - - - - -
                              | | | | | | -
                              - - - - - -   -
                              | | | | | |     -
                              - - - - - -       -        - - - 
                              | | | | | |          }---> | | |
                              - - - - - -       -        - - -
                              | | | | | |     -          | | |
                              - - - - - -   -            - - -
                              | | | | | | - 
                              - - - - - -
  - -
  | | each of these boxes is a neuron, in this example we took window of 2x2 of neurons on leftside squares to form one 
  square on rightside squares. There is no overlap and one column on right and one row on bottom of leftside squares
  - -
   arguments are window, mapp, weight,delay,overlap
   The structure of list here is [pre_syn_neuron, post_syn_neuron, weight, axonal_delay]
    [(0, 0, 1, 1), (1, 0, 1, 1), (4, 0, 1, 1), (5, 0, 1, 1), (2, 1, 1, 1), (3, 1, 1, 1), (6, 1, 1, 1), (7, 1, 1, 1),
    (8, 2, 1, 1), (9, 2, 1, 1), (12, 2, 1, 1), (13, 2, 1, 1), (10, 3, 1, 1), (11, 3, 1, 1), (14, 3, 1, 1), (15, 3, 1, 1)]
This code can also be used for convolving populations. For performing convolution just enter the overlap value:
window-1'''
    conn_list = [(0,0,1,1)]
    def __init__(self,window,mapp,weight,delay,overlap):
        self.window = window
        self.mapp = mapp
        self.weight = weight
        self.delay = delay
        self.overlap = overlap
         	
    
    
    
    def PoolConv(self):
        
        ''' this method implements the logic for pooling/convolution. If overlap is window-1 then it's convolution.'''
        extra = int(math.floor((self.mapp-self.window)/(self.window-self.overlap)+1))
        
        for p in range(0,self.window-1):   
            w = self.conn_list[p][0]+1  
            v = self.conn_list[p][1]
            q = self.weight
            s = self.delay
            self.conn_list.append((w,v,q,s))


        for c in range(0,(self.window-1)*self.window):    
            x = self.conn_list[c][0] + self.mapp  
            y = self.conn_list[c][1]
            q = self.weight
            s = self.delay
            self.conn_list.append((x,y,q,s))

        skip = []
        for p in range(0,extra*extra):
            skip.append((p+1)*extra-1)    
        
                                                           
        for i in range(0,extra*extra-1):     
            if(i in skip):                 
                z = skip.index(i)
                for k in range(0+(self.window**2)*i,(self.window**2)+(self.window**2)*i):   
                    z = self.conn_list[(self.window**2)*skip[0]][0]
                    n = (self.conn_list[k][0] + self.mapp*(self.window-self.overlap)) -z   
                    m = self.conn_list[k][1] + 1  
                    q = self.weight
                    s = self.delay
                    new_item= (n,m,q,s)
                    self.conn_list.append(new_item)             

            else:
                for j in range(0+(self.window**2)*i,(self.window**2)+(self.window**2)*i):
                    a = self.conn_list[j][0] +self.window-self.overlap     
                    b = self.conn_list[j][1] +1
                    q = self.weight
                    s = self.delay
                    list1 = (a,b,q,s)
                    self.conn_list.append(list1)
                    

c = poolconv(3,5,1,1,1)

