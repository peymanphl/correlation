
from threading import Thread
import paramiko
import time 
#from scipy.stats.stats import pearsonr
import numpy as np


def destination(host,i, itr, max_tx, error_node):
	print "i {} ".format(i)
	filename = "f"
	f=open(filename,'w')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("./correlation --type=destination  --id={} --iteration={}".format(i, itr))
	#data = f.read()

	
#	if (stderr):
#		print ("error:", stderr.read())

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

	print ("finished" , i)
	print "####################################################################"

def source(host,i, itr, max_tx, error_node):
	filename = "f"
	f=open(filename,'w')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("./correlation --type=source --max_tx={} --id={} --rate=5 --iteration={}".format(max_tx, i, itr))




