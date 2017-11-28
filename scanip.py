#!/usr/bin/python
#_*_coding:utf-8 _*_
import IPy,sys,subprocess,time,getopt
from multiprocessing import Pool

VERSION = "v0.1-beat"
POOL_SIZE = 500

def mping(host):
	if sys.platform == "win32":
		cmd = ("ping -n 1 " +host).split(" ")
	elif sys.platform == "linux2":
		cmd = ("ping -c 1 -q " +host).split(" ")
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	time.sleep(1)	#停止1秒，等待程序运行
	if p.poll() == 0:
		return(host,"Up")
	else:
		p.kill()
		return(host,"Down")

def start_scan(ip_list):
	p = Pool(POOL_SIZE)
	res = p.map(mping, ip_list)
	p.close()
	p.join()
	return res

def scan_net(net):
	try:
		ip_net = IPy.IP(net)
	except ValueError:
		print("Error: incorret ip address or subnet")
		exit(1)
	ip_list=[]
	if ip_net.len() == 1:
		ip_list.append(str(ipaddr))
	else:
		for ipaddr in ip_net[1:ip_net.len()-1]:	#地址范围不包含网段号与广播地址
			ip_list.append(str(ipaddr))
	return(start_scan(ip_list))

def scan_range(range):
	net_slice=range.split(".")
	if len(net_slice) == 4:
		net_prefix = net_slice[0] + "." + net_slice[1] + "." + net_slice[2]
	else:
		pass

	range_slice = net_slice[3].split("-")
	if len(range_slice) == 2:
		range_first = int(range_slice[0])
		range_last = int(range_slice[1])
	else:
		pass
	
	ip_list=[]
	try:
		ip_net=IPy.IP(net_prefix+".0/24")
		for ipaddr in ip_net[range_first:range_last+1]:
			ip_list.append(str(ipaddr))
	except ValueError:
		pass
	return(start_scan(ip_list))

def scan_urlfile(urlfile):
	pass

opts, args = getopt.getopt(sys.argv[1:],'-hv',["net=","range=","urlfile="])
for name, value in opts:
	if name == "-h":
		print("help func")
	if name == "--net":
		print(scan_net(value))
	if name == "--range":
		print(scan_range(value))
	if name == "--urlfile":
		print("urlfile func")
	if name == "-v":
		print(VERSION)

