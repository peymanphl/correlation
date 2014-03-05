from threading import Thread
import paramiko
import time 
from scipy.stats.stats import pearsonr
import numpy as np

def destination(host,i):
	global max_tx
	print "i {} ".format(i)
	filename = "f"
	f=open(filename,'w')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("./correlation --type=destination  --id={} --rate=5".format( i))
	#data = f.read()
	print "finished"
	loss = 0 
	ID = 00
	error = [0]*max_tx
	print "hi"	
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


src = "rasp02"
src_id = 1

des = "rasp05"
des_id = 3

des1 = "rasp10"
des1_id = 4

des2 = "rasp09"
des2_id = 5
max_tx = 1000000


iteration = 1000

import pickle 
import os
filename = "correlation.pck"
if os.path.exists(filename):
    os.remove(filename)

for i in range (1, iteration):
			

	error_node = list()

	source_th = Thread(target = source, args = (src, src_id))
	destination_th = Thread(target = destination, args = (des, des_id))
	destination_th1 = Thread(target = destination, args = (des1, des1_id))
	destination_th2 = Thread(target = destination, args = (des2, des2_id))


	destination_th.start();
	destination_th1.start();
	destination_th2.start();

	time.sleep(2)

	source_th.start()

	source_th.join()
	destination_th.join()
	destination_th1.join()
	destination_th2.join()
	
	f = open (filename, 'a')
	pickle.dump(error_node, f)
	f.close()
	print error_node[0]
	print error_node[1]

	print pearsonr(error_node[0], error_node[1])
	print pearsonr(error_node[1], error_node[2])
	print pearsonr(error_node[0], error_node[2])



