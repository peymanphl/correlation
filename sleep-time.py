from threading import Thread
import paramiko
import time 
from scipy.stats.stats import pearsonr
import numpy as np
import subprocess as proc

def monitor_trrafic(host):

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f1, stderr = ssh.exec_command("sudo ./tcpdump.sh")
	if stderr:
		print(stderr.read())



def kill(host):

	time.sleep(10)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='pi', password='rasp')
	stdin, f, stderr = ssh.exec_command("sudo ./kill_tcpdump.sh")
	if stderr:
		print(stderr.read())

def listen():
	f = open("tcpdump","w")
	p = proc.Popen(["nc", "-l", "8899"], stdout=f )
	p.wait()
	f.close()
	f = open("data_rate","rw") 
	result = proc.Popen(["capinfos","-T","-i","tcpdump"], stdout=f)
	
	line = f.readline()
	line = f.readline()
	a = line.split("\t")
	print a[0]
	print a[1]
	return a[1]
"""
monitor = "rasp05.lab.es.aau.dk"

mon = Thread(target = monitor_trrafic, args = (monitor,))
kill_server = Thread(target = kill, args = (monitor,))
listen_server = Thread(target = listen)

listen_server.start()
time.sleep(2)

mon.start()
time.sleep(5)
kill_server.start()
listen_server.join()
"""
