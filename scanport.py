#!/usr/bin/python
#_*_coding:utf-8 _*_
import socket,IPy,sys,subprocess,time,getopt
from multiprocessing import Pool

VERSION = "v0.1-beat"
POOL_SIZE = 500
LOG_FILE_PATH = "./scanport.csv"

def portsniff(host_ipaddr, port_number):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(2)
	addr=(host_ipaddr, port_number)
	try:
		s.connect(addr)
		s.close()
	except socket.error:
		print('time out')
portsniff('172.20.1.1',23)