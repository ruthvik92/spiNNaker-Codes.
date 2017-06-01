
#this code does pooling without overlap. parameters are set for 5x5 map and 2x2 pooling window.
## The initial window is also formed automatically. ###this works for 2x2 pooling and 5x5 input map. still coding for general cases
window = int(raw_input('Enter the size of the pooling window row(column):'))
mapp= int(raw_input('Enter the size of the input map row(column):'))

#form the initial window
conn_list = [(0,0)]
for p in range(0,window-1):   ##windows size is 2x2 here so loop only once to append one item.
    w = conn_list[p][0]+1  ##this number is 1 cos we're moving right by 1 neuron.
    v = conn_list[p][1]
    conn_list.append((w,v))


for c in range(0,(window-1)*window):     ###loop twice(2x2) to get the the blocks on the second row. 
    x = conn_list[c][0] + mapp   ##this number is 5 cos we're moving to next row of neurons(5x5 map).
    y = conn_list[c][1]
    conn_list.append((x,y))

print conn_list

## form the rest of the mapping(pooling).
skip = []
for p in range(0,mapp-1):
    skip.append(window-1+p*window)    ##these numbers say when to skip to the next row. Here the count starts from 
                              ##0. map is 5x5 and window is 2x2.
for i in range(0,(mapp/window)*(mapp/window)-1):    ####this gives number of full squares in 5x5 map.    
    if(i in skip):                  ### if we reach the count we should skip to next row.
        print 'skip'
        print i
        z = skip.index(i)
        for k in range(0+(window**2)*i,(window**2)+(window**2)*i):   ### since our map is 2x2 there are 4 elements in the map henceforth 4.
            n = conn_list[k][0] + window*(mapp-1)   ####this gives the skip 2 rows when going down. 2 rows so 2*4(added to the 5th item of previous row)  
            m = conn_list[k][1] + 1   ## this is move to right.
            new_item= (n,m)
            conn_list.append(new_item)             

    else:
        for j in range(0+(window**2)*i,(window**2)+(window**2)*i):
            #@print i
            a = conn_list[j][0] +window      ###this gives skip to next non overlapping area in the same row. map is 2x2.
            b = conn_list[j][1] +1     
            list1 = (a,b)
            conn_list.append(list1)
            #@print conn_list
