#!/usr/bin/python
#_*_coding:utf-8 _*_
import IPy,sys,subprocess,time,getopt

# ipaddr="www.baidu.com"
# try:
# 	ip_range = IPy.IP(ipaddr)
# except ValueError:
# 	print("Error: incorret ip address or subnet")

# if ip_range.len() == 1:
# 	print ip_range
# else:
# 	for ipaddr in ip_range[1:ip_range.len()-1]:	#地址范围不包含网段号与广播地址
# 		print ipaddr

def mping(host):
	if sys.platform == "win32":
		cmd = ("ping -n 1 " +host).split(" ")
	elif sys.platform == "linux2":
		cmd = ("ping -c 1 -q " +host).split(" ")
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	time.sleep(1)	#停止1秒，等待程序运行
	if p.poll() == 0:
		return(host,0)
	else:
		p.kill()
		return(host,1)

opts, args = getopt.getopt(sys.argv[1:],'-hv',["net=","range=","urlfile="])
for name, value in opts:
	if name == "-h":
		print("help func")
