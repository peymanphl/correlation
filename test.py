from correlation import *
from traffic_mon import *
import pickle 
import os
import time
import datetime
import Queue


src = "rasp00.lab.es.aau.dk"
src_id = 5

des = list()
des_id = range (0,5)

des.insert(0, "rasp01.lab.es.aau.dk")
des.insert(1, "rasp02.lab.es.aau.dk")
des.insert(2, "rasp03.lab.es.aau.dk")
des.insert(3, "rasp04.lab.es.aau.dk")
des.insert(4, "rasp06.lab.es.aau.dk")

monitor = "rasp05.lab.es.aau.dk"
time_out = 100
max_des = 5
max_tx = 100
iteration = 10000
log = "log.pck"
Result = Queue.Queue()
start_time = time.time() 
max_time = time.time() + 60*time_out

for i in range (1, iteration):
	
	if time.time()  > max_time:	
		break;

	start_time = datetime.datetime.today()
        mon = Thread(target = monitor_trrafic, args = (monitor,))
        kill_server = Thread(target = kill, args = (monitor,))
        listen_server = Thread(target = listen, args = (Result,))
	
	error_node = list()
	destination_th = []

	source_th = Thread(target = source, args = (src, src_id, i, max_tx, error_node))
	for j in range (0, max_des):
		t =  Thread(target = destination, args = (des[j], des_id[j], i, max_tx, error_node))
		destination_th.append(t)

	[x.start() for x in destination_th]

	listen_server.start()

	time.sleep(2)
        
	mon.start()
	
	source_th.start()

	source_th.join()

	[x.join() for x in destination_th]

	print "finished total" 
	end_time = datetime.datetime.today()
	
        kill_server.start()
        listen_server.join()
      	data_rate = Result.get()/(1024*8)
	print ("data rate", data_rate)

	if os.path.exists(log):				
		f = open(log, "a")
	else:
		
		f = open(log, "w")


	pickle.dump(error_node, f)
	pickle.dump(start_time, f)
	pickle.dump(end_time, f)
	pickle.dump(data_rate, f)
	f.close()
        print error_node

	print pearsonr(error_node[0], error_node[1])
	print pearsonr(error_node[0], error_node[2])
	print pearsonr(error_node[0], error_node[3])
	print pearsonr(error_node[0], error_node[4])


