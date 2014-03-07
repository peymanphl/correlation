import pickle 
import numpy as np
from scipy.stats.stats import pearsonr
import pandas as pd
import collections

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def burst(error):

	last = 1
	i = 0
	count = 1
	
	burst_index = list()
	burst_lenght = list()
	
	a = np.array(100)

	for v in error:
	    if v == 0 and last == 1:
		#print("new: ", i)
		burst_index.append(i)
	    elif v == 1 and last == 0:
		#print("count: ", count)
		burst_lenght.append(count)

		count = 1
	    elif v == 0 and last == 0:
		count += 1

	    last = v
	    i += 1

	if v == 0:
	   # print("count: ", count)
	    burst_lenght.append(count)

	#print burst_lenght
	sample = burst_lenght[0:1000000]

	table = list()
	for j in range (1, 10):
		b = list()
		a =  list_duplicates_of(sample, j)
		for k in range (0, len(a)):
			b.append(a[k])

		table.insert(j,b)
	#print "tamam"
	#print table
	return table[0]

	
	


filename = "log.pck"
f = open (filename, "rb")
nodes = 5 


data = list()

er = [0,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0]

burst(er)

print 'Load data...'
try:
	 while True: # load from the file until EOF is reached
		 error_node = pickle.load(f)
		 start_time= pickle.load(f)
		 end_time = pickle.load(f)
		 data_rate = pickle.load(f)
		
		 for i in range (0, nodes):
			 for j in range(0, nodes):
				# print (i, " ", j)
				 co = collections.Counter(error_node[i])
				 val = co.values()
				 loss = float(val[0])/len(error_node[0])
				 if loss == 1.0 and len(co) == 1:
					 loss=0
				 data.append( {'c1': i, 'c2': j, 'rate': data_rate, 'start': start_time, 'end': end_time, 'corre': pearsonr(error_node[i], error_node[j])[0], 'p':pearsonr(error_node[i], error_node[j])[1], 'loss':loss})


		# print 'loaded: '
		 
except EOFError:
	  print 'End of file reached'
	  f.close()

df = pd.DataFrame(data)

a = df.query('c1 == 0 and c2 == 1')
#print df
#a =df[ df.c1==1 and df.c2==2]

print a[ ['corre','c1'] ]

b = df[ (df['c1'] == 0) & (df['c2'] == 1) ]
print b.corre

#print burst(error_node[1])
#print burst(error_node[2])
"""
c1 = np.array(c1)
c2 = np.array(c2)
c3 = np.array(c3)


print np.mean(c1)
print np.mean(c2)
print np.mean(c3)

"""

