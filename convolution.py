import math
window = int(raw_input('Enter the size of the convolving window row(column):'))
mapp= int(raw_input('Enter the size of the input map row(column):'))
weight = int(raw_input('Enter the weight value for pooling(enter 1):'))
delay = int(raw_input('Enter the delay value, its in milli seconds:'))
window_ceil = int(math.ceil(window/2.0))
    #form the initial window
conn_list = [(0,0,1,1)]
for p in range(0,window-1):   ##windows size is windowxwindow here so loop window-1 times to append items.
    w = conn_list[p][0]+1  ##this number is 1 cos we're moving right by 1 neuron.
    v = conn_list[p][1]
    q = weight
    s = delay
    conn_list.append((w,v,q,s))


for c in range(0,(window-1)*window):     ###loop twice(2x2) to get the the blocks on the second row. 
    x = conn_list[c][0] + mapp   ##this number is 5 cos we're moving to next row of neurons(5x5 map).
    y = conn_list[c][1]
    q = weight
    s = delay
    conn_list.append((x,y,q,s))

## form the rest of the mapping(pooling). Don't know if will be used.
#skip = []
#for q in range(0,mapp-window_ceil):
#    skip.append((mapp-window_ceil)*(q+2)+2*(q+1))

skip =[]
for q in range(0,mapp-window_ceil):
    skip.append((mapp-window_ceil)*(q+1)-1)

for i in range(0,(mapp-window_ceil)*(mapp-window_ceil)-1):    ####this gives number of full squares in 5x5 map.    
        if(i in skip):                  ### if we reach the count we should skip to next row.
            #print 'skip and i:'
            #print i
            z = skip.index(i)
            for k in range(0+(window**2)*i,(window**2)+(window**2)*i):   ### since our map is 2x2 there are 4 elements in the map henceforth 4.
                #print conn_list
                n = conn_list[k][0] + window   ####this gives the skip 2 rows when going down. 2 rows so 2*4(added to the 5th item of previous row)  
                m = conn_list[k][1] + 1   ## this is move to right.
                q = weight
                s = delay
                new_item= (n,m,q,s)
                conn_list.append(new_item)
                #print conn_list
                #print i

        else:
            for j in range(0+(window**2)*i,(window**2)*(i+1)):
                #print "no skip and i:"
                #print i
                #print conn_list
                a = conn_list[j][0] +1      ###this gives skip to next non overlapping area in the same row. map is 2x2.
                b = conn_list[j][1] +1
                #b =i
                q = weight
                s = delay
                list1 = (a,b,q,s)
                conn_list.append(list1)
                print conn_list
                print i

