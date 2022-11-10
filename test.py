"""
Custom topology example
Two directly connected switches plus a host for each switch:
host --- switch --- switch --- host
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
start OVS Test Controller as:
sudo ovs-controller --max-idle=500 ptcp:6633:127.0.0.2
To add delay and redirect traffic, follow instructiosn from link:
https://mailman.stanford.edu/pipermail/mininet-discuss/2014-January/003882.html
"""
import signal
import sys
import subprocess
import os
import enum
import datetime
import dpkt

import pingparsing

from scapy.all import *
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Controller, OVSSwitch
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

class topology(Topo):

    def build(self):

        h1  = self.addHost('h1', mac='0a:55:76:65:cd:f0',ip="192.168.1.1/24")
        h2  = self.addHost('h2', mac='0a:55:76:65:cd:f1',ip="192.168.1.2/24")
        h3  = self.addHost('h3', mac='0a:55:76:65:cd:f2',ip="192.168.1.3/24")
        h4  = self.addHost('h4', mac='0a:55:76:65:cd:f3',ip="192.168.1.4/24")
        h5  = self.addHost('h5', mac='0a:55:76:65:cd:f4',ip="192.168.1.5/24")
        h6  = self.addHost('h6', mac='0a:55:76:65:cd:f5',ip="192.168.1.6/24")

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        #c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.2', port=6633)

        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s3)
        self.addLink(h5, s1)
        self.addLink(h6, s1)


if __name__ == '__main__':
    setLogLevel( 'info' )
    topo = topology()
    c0 = RemoteController('c0', ip='127.0.0.2', port=5555)
    net = Mininet(topo=topo, controller=c0)
    net.start()
   
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    s1 = net.get('s1')
    s2 = net.get('s2')
    s3 = net.get('s3')
   
    d = {}
    sleep(2)
    c_1 = []
    '''
    for i in range(102):
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s3 priority=0,actions=CONTROLLER:65535")
    print(c_1)
    c_1 = []
    for i in range(102):
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=3,in_port=3,dl_src=0a:55:76:65:cd:f4,dl_dst=0a:55:76:65:cd:f0,actions=output:1")
    print(c_1)
    c_1 = []
    for i in range(102):
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f4,dl_dst=0a:55:76:65:cd:f0,actions=output:2")
       
        case 1 all miss
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        h1.cmd("ip ne flush all")
        h5.cmd("ip ne flush all")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s1 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s3 priority=0,action=CONTROLLER:65535")
        case 2
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])    

        case 3
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s1 priority=0,action=CONTROLLER:65535")

        case 4
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")

        case 5
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f4,dl_dst=0a:55:76:65:cd:f0,actions=output:2")

        case 8
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        sleep(0.5)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=1,in_port=2,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f4,actions=output:1")

        #case 6
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f4,actions=output:3")

        #case 7
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=3,dl_dst=0a:55:76:65:cd:f0,dl_src=0a:55:76:65:cd:f4,actions=output:1")

        case 9
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=3,dl_dst=0a:55:76:65:cd:f0,dl_src=0a:55:76:65:cd:f4,actions=output:1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f4,dl_dst=0a:55:76:65:cd:f0,actions=output:2")
        sleep(0.1)

        case 10
        p = h1.popen("ping -c 1 192.168.1.5")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535")
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f4,actions=output:3")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=1,in_port=2,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f4,actions=output:1")      
        sleep(0.1)

        h1_pid = h1.cmd("tcpdump host 192.168.1.5 -Qout -w send.pcap &");
        print(h1.cmd("pwd"))
        print("!", h1_pid)
        h1_pid = h1_pid.split(" ")
        h1_pid = h1_pid[1]
        sleep(1)
        recv = h1.cmd("tcpdump host 192.168.1.5 -Qin -w recv.pcap &");
        print(h1.cmd("pwd"))
        print("!", recv)
        recv = recv.split(" ")
        recv = recv[1]    
       
        h1.cmdPrint("ping 192.168.1.5 -c 1")
   
        send = ''
        s = []
        sleep(1)
        h1.cmd("sudo kill -9 {}".format(h1_pid))
        sleep(1)
        out = h1.cmd("sudo tcpdump -r send.pcap")
        sleep(1)
        print("out ", out)
        h1.cmd("sudo kill -9 {}".format(recv))
        out = h1.cmd("sudo tcpdump -r recv.pcap")
        sleep(1)
        print("out ", out)
        with open('send.pcap', 'rb') as f:
            send = dpkt.pcap.Reader(f)
            for ts,buf in pcap:
                s.append(datetime.datetime(ts))
       
        print("cmd ", cmd)      
        #s.cmd()
        print("!", h1_pid)
        sleep(0.1)
        for i in range(102):

    for i in range(102):

        #case 9-14
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        sleep(0.2)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s1 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s3 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s2 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f2,dl_dst=0a:55:76:65:cd:f0,actions=output:2")
        #s1.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f2,actions=output:2")
        #s3.cmd("sudo ovs-ofctl -O OpenFlow14 add-flow s1 priority=1,in_port=1,dl_src=0a:55:76:65:cd:f0,dl_dst=0a:55:76:65:cd:f2,actions=output:2")

        # case 6,7,8
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])

        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        sleep(0.2)
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s3 priority=0,action=CONTROLLER:65535")
        sleep(0.2)
        # case 3,4,5
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])

        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        sleep(0.2)
        s3.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s3 priority=0,action=CONTROLLER:65535")
        sleep(0.2)
        case 2
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])

        sleep(0.1)
        case 1
        p = h1.popen("ping -c 1 192.168.1.3")
        out, err = p.communicate( timeout=5)
        p.terminate()
        out = out.decode('utf-8')
        parse = pingparsing.PingParsing()
        ddd = parse.parse(out)
        dd = ddd.as_dict()
        c_1.append(dd['rtt_avg'])
       
        s1.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s1")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s2")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14 del-flows s3")
        h1.cmd("ip ne flush all")
        h3.cmd("ip ne flush all")
        sleep(0.5)
        s1.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s1 priority=0,action=CONTROLLER:65535")
        s2.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s2 priority=0,action=CONTROLLER:65535")
        s3.cmd("sudo ovs-ofctl -O OpenFlow14  add-flow s3 priority=0,action=CONTROLLER:65535")
        sleep(0.1)
        '''

    print("list ", c_1)
    CLI(net)
