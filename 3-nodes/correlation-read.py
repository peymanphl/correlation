import pickle 
import numpy as np
from scipy.stats.stats import pearsonr

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

	
	


filename = "correlation-far.pck"
f = open (filename, "rb")

c1 =  list()
c2 = list ()
c3 = list()

data = list()

er = [0,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0]

burst(er)

print 'Load data...'
try:
	 while True: # load from the file until EOF is reached
		 error_node = pickle.load(f)
		 c1. append(pearsonr(error_node[0], error_node[1])[0])
		 c2. append(pearsonr(error_node[1], error_node[2])[0])
		 c3. append(pearsonr(error_node[0], error_node[2])[0])
		 print 'loaded: '
		 data.append(error_node)
		 break;
except EOFError:
	  print 'End of file reached'
	  f.close()




import collections
co = collections.Counter(error_node[0])
val = co.values()
print co 
print len(error_node[0])
print float(val[0])/len(error_node[0])

#print burst(error_node[1])
#print burst(error_node[2])

c1 = np.array(c1)
c2 = np.array(c2)
c3 = np.array(c3)

h = list()
for k in range(1, 2):
	for j in range(0, 3):
		for i in range(0*k,101*k):
			if error_node[j][i] == 1:
				h.append(i/k);
			
#print h

c = np.array(error_node[0][1:100])+  np.array(error_node[1][1:100])+ np.array(error_node[2][1:100]) 

#print  c 

print np.mean(c1)
print np.mean(c2)
print np.mean(c3)


import pylab as p

bins = range(1,101)
#print bins 
#n, bins, patches = p.hist(np.array(h)*100, bins, normed=1, histtype='bar', rwidth=0.8)
p.hist(h, bins)
#p.show();

