def pooling():
    
    '''code tested for       |map     |window    |
                             |5       | 2        |
                             |9       | 3        |
                             |9       | 2        |
                             |9       | 4        |
                             |9       | 5        |
                             |10      | 2        |
                             |10      | 3        |
                             |4       | 2        |
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
  | | each of these boxes is a neuron, in this example we took window of 2x2 neurons on leftside squares to form one square on 
  - - rightside squares. There is no overlap and one column on right and one row on bottom of leftside squares to form 2x2 on 
  right. The structure of list here is[pre_syn_neuron, post_syn_neuron, weight, axonal_delay]
Sample output:
Enter the size of the pooling window row(column):2
Enter the size of the input map row(column):4
Enter the weight value for pooling(enter 1):1
Enter the delay value, its in milli seconds:1
[(0, 0, 1, 1), (1, 0, 1, 1), (4, 0, 1, 1), (5, 0, 1, 1), (2, 1, 1, 1), (3, 1, 1, 1), (6, 1, 1, 1),
(7, 1, 1, 1), (8, 2, 1, 1), (9, 2, 1, 1), (12, 2, 1, 1), (13, 2, 1, 1), (10, 3, 1, 1), (11, 3, 1, 1), 
(14, 3, 1, 1), (15, 3, 1, 1)]'''
    #this code does pooling without overlap. parameters are set for 5x5 map and 2x2 pooling window.
    ## The initial window is also formed automatically. ###this works for 2x2 pooling and 5x5 input map. still coding for general cases
    window = int(raw_input('Enter the size of the pooling window row(column):'))
    mapp= int(raw_input('Enter the size of the input map row(column):'))
    weight = int(raw_input('Enter the weight value for pooling(enter 1):'))
    delay = int(raw_input('Enter the delay value, its in milli seconds:'))

    #form the initial window
    conn_list = [(0,0,1,1)]
    for p in range(0,window-1):   ##windows size is 2x2 here so loop only once to append one item.
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

    #print conn_list

    ## form the rest of the mapping(pooling).
    skip = []
    for p in range(0,mapp/window):
        skip.append((mapp/window)-1+p*(mapp/window))    ##these numbers say when to skip to the next row. Here the count starts from 
                                  ##0. map is 5x5 and window is 2x2.
    for i in range(0,(mapp/window)*(mapp/window)-1):    ####this gives number of full squares in 5x5 map.    
        if(i in skip):                  ### if we reach the count we should skip to next row.
            #print 'skip and i:'
            #print i
            z = skip.index(i)
            for k in range(0+(window**2)*i,(window**2)+(window**2)*i):   ### since our map is 2x2 there are 4 elements in the map henceforth 4.
                #print conn_list
                n = conn_list[k][0] + window*(mapp-skip[0])   ####this gives the skip 2 rows when going down. 2 rows so 2*4(added to the 5th item of previous row)  
                m = conn_list[k][1] + 1   ## this is move to right.
                q = weight
                s = delay
                new_item= (n,m,q,s)
                conn_list.append(new_item)             

        else:
            for j in range(0+(window**2)*i,(window**2)+(window**2)*i):
                #print "no skip and i:"
                #print i
                #print conn_list
                a = conn_list[j][0] +window      ###this gives skip to next non overlapping area in the same row. map is 2x2.
                b = conn_list[j][1] +1
                q = weight
                s = delay
                list1 = (a,b,q,s)
                conn_list.append(list1)
                #@print conn_list
    return conn_list

print pooling()
