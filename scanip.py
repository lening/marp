#!/usr/bin/python
#_*_coding:utf-8 _*_
import IPy,sys,subprocess,time,getopt
from multiprocessing import Pool

VERSION = "v0.1-beat"
POOL_SIZE = 500
LOG_FILE_PATH = "./scanip.csv"

#获取目标主机扫描结果
def mping(host):
	if sys.platform == "win32":
		cmd = ("ping -n 1 " +host).split(" ")
	elif sys.platform == "linux2":
		cmd = ("ping -c 1 -q " +host).split(" ")
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	time.sleep(2)	#停止2秒，等待程序运行
	if p.poll() == 0:
		return(host,"Up")
	else:
		p.kill()
		return(host,"Down")

#执行多进程扫描
def start_scan(host_list):
	p = Pool(POOL_SIZE)
	res = p.map(mping, host_list)
	p.close()
	p.join()
	return res

#按网段扫描
def scan_net(net):
	try:
		ip_net = IPy.IP(net)
	except ValueError:
		error_exit(scan_net.__name__,1)
	ip_list=[]
	if ip_net.len() == 1:
		ip_list.append(str(ipaddr))
	else:
		for ipaddr in ip_net[1:ip_net.len()-1]:	#地址范围不包含网段号与广播地址
			ip_list.append(str(ipaddr))
	return(start_scan(ip_list))

#按IP地址范围扫描
def scan_range(range):
	net_slice=range.split(".")
	if len(net_slice) == 4:
		net_prefix = net_slice[0] + "." + net_slice[1] + "." + net_slice[2]
	else:
		error_exit(scan_range.__name__,1)

	range_slice = net_slice[3].split("-")
	if len(range_slice) == 2:
		range_first = int(range_slice[0])
		range_last = int(range_slice[1])
	else:
		error_exit(scan_range.__name__,1)
	
	ip_list=[]
	try:
		ip_net=IPy.IP(net_prefix+".0/24")
		for ipaddr in ip_net[range_first:range_last+1]:
			ip_list.append(str(ipaddr))
		return(start_scan(ip_list))
	except ValueError:
		error_exit(scan_range.__name__,1)

#读取文件扫描
def scan_urlfile(urlfile_path="./url.conf"):
	try:
		with open(urlfile_path,'r') as hostfile:
			host_list = []
			for host in hostfile:
				host_list.append(host.strip('\n\r'))
			return(start_scan(host_list))
	except IOError:
		error_exit(scan_urlfile.__name__,2)		

class WriteData(object):
	def __init__(self, data_list):
		self.data_list = data_list

#将数据写入到sqlite数据库
	def to_sqliteDB(self):
		try:
			import sqlite3
		except ImportError:
			error_exit(to_sqliteDB.__name__,3)
		conn = sqlite3.connect(DB_PATH)
		cu = conn.cursor()	
		for data in self.data_list:
			sql = "INSERT INTO HOST_LATENCY (RECORD_TIME,HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(data[0], data[1])
			cu.execute(sql)
			conn.commit()
		conn.close()

#将数据写入到log文件
	def to_logfile(self):			
		try:
			with open(LOG_FILE_PATH,'a') as logfile:
				for data in self.data_list:
					if 	data[1] == "Down":
						continue
					else:
						msg = data[0] + "," + data[1] + '\n'
						logfile.write(msg)
		except IOError:
			error_exit(to_logfile.__name__,2)
#错误处理
def error_exit(error_str,error_code):
	if error_code == 1:		#IP地址或网段不合法
		print("Error in %s: incorret ip address or subnet"%(error_str))
		exit(1)
	elif error_code == 2:	#打开文件失败
		print("Error in %s: Open file failed, please check it..."%(error_str))
		exit(2)
	elif error_code == 3:	#导入模块失败
		print("Error: import %s failed, please check it..."%(error_str))
		exit(3)

def help():
	print("选项:")
	print("    -h           显示帮助选项")
	print("    -v           显示程序版本")
	print("    --net=       按指定网段进行扫描，如: ./scanip.py --net=192.168.1.0/24")
	print("    --range=     按指定IP地址范围进行扫描，如: ./scanip.py --net=192.168.1.1-100")
	print("    --urlfile=   读取指定文件中的URL进行扫描，每行一个URL，如: ./scanip.py --urlfile=url.conf")

def main():
	opts, args = getopt.getopt(sys.argv[1:],'-hv',["net=","range=","urlfile="])
	for name, value in opts:
		if name == "-h":
			help()
		elif name == "--net":
			data=WriteData(scan_net(value))
			data.to_logfile()
		elif name == "--range":
			data=WriteData(scan_range(value))
			data.to_logfile()
		elif name == "--urlfile":
			data=WriteData(scan_urlfile(value))
			data.to_logfile()
		elif name == "-v":
			print(VERSION)
	
if __name__ == '__main__':
	main()