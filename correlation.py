
from threading import Thread
import paramiko
import time 
from scipy.stats.stats import pearsonr
import numpy as np
from traffic_mon import *


def destination(host,i):
	global max_tx
	print "i {} ".format(i)
	filename = "f"
	f=open(filename,'w')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("./correlation --type=destination  --id={} --rate=20".format( i))
	#data = f.read()
	print "finished"
	loss = 0 
	ID = 00
	error = [0]*max_tx
	while True:
		line=f.readline()
		if not line:
			break
		line=line.split(":")
		if line[0] == "ID":
			ID = int(line[1].strip())	
		if line[0] == "seq":
			error[int(line[1].strip())] = 1
		if line[0] == "loss":
			loss = float(line[1].strip())
			print "node ID: {}".format(i)		
			print "loss {} {}".format(ID, loss)
	error_node.insert(i, error)
	print len (error)
	print "####################################################################"
def source(host,i):
	global max_tx
	filename = "f"
	f=open(filename,'w')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("./correlation --type=source --max_tx={} --id={} --rate=5".format(max_tx, i))
	print "source finished"


src = "rasp02.lab.es.aau.dk"
src_id = 1

des = "rasp01.lab.es.aau.dk"
des_id = 2

des1 = "rasp10.lab.es.aau.dk"
des1_id = 3


des3 = "rasp00.lab.es.aau.dk"
des3_id = 6

des4 = "rasp03.lab.es.aau.dk"
des4_id = 7

des5 = "rasp08.lab.es.aau.dk"
des5_id = 8

monitor = "rasp05.lab.es.aau.dk"




max_tx = 1000


iteration = 50

import pickle 
import os
import time
import datetime
import Queue

filename = "correlation-6node.pck"
if os.path.exists(filename):
    os.remove(filename)

Result = Queue.Queue()
for i in range (1, iteration):
	
	
	start_time = datetime.datetime.today()
        mon = Thread(target = monitor_trrafic, args = (monitor,))
        kill_server = Thread(target = kill, args = (monitor,))
        listen_server = Thread(target = listen, args = (Result,))

	error_node = list()


	source_th = Thread(target = source, args = (src, src_id))
	destination_th = Thread(target = destination, args = (des, des_id))
	destination_th1 = Thread(target = destination, args = (des1, des1_id))
#	destination_th3 = Thread(target = destination, args = (des3, des3_id))
#	destination_th4 = Thread(target = destination, args = (des4, des4_id))
#	destination_th5 = Thread(target = destination, args = (des5, des5_id))
#	destination_th6 = Thread(target = destination, args = (des6, des6_id))


	destination_th.start();
	destination_th1.start();
#	destination_th3.start();
#	destination_th4.start();
#	destination_th5.start();
#	destination_th6.start();
	listen_server.start()


	time.sleep(2)
        mon.start()
	source_th.start()

	source_th.join()
	destination_th.join()
	destination_th1.join()
#	destination_th3.join()
#	destination_th4.join()
#	destination_th5.join()
#	destination_th6.join()

        kill_server.start()
        listen_server.join()
	end_time = datetime.datetime.today()
        #print ("data_rate ", Result.get()/(1024*8), " KB")
	data_rate = Result.get()/(1024*8)
	
	if os.path.exists(log_completion_time ):				
		f = open(log_completion_time, "a")
	else:
		
		f = open(log_completion_time, "w")


	pickle.dump(error_node, f)
	pickle.dump(start_time, f)
	pickle.dump(end_time, f)
	pickle.dump(data_rate, f)
	f.close()
 #       print error_node[0]
#	print error_node[1]
#	print error_node[2]
#	print error_node[3]
#	print error_node[4]
#	print error_node[5]

	print pearsonr(error_node[0], error_node[1])
"""	print pearsonr(error_node[0], error_node[2])
	print pearsonr(error_node[0], error_node[3])
	print pearsonr(error_node[0], error_node[4])
	print pearsonr(error_node[0], error_node[5])

"""

