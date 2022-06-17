#!/usr/bin/python
from multiprocessing.sharedctypes import Value
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from time import time
from mininet.util import pmonitor
from signal import SIGINT
from subprocess import Popen, PIPE
import os

class MyTopo(Topo):
    '''Topology to be instantiated in Mininet'''
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        #Define bandwidth
        bw1 = 1
        bw2 = 0.5

        #Creating the nodes/hosts
        hostA = self.addHost('hostA') 
        hostB = self.addHost('hostB')
        
        #Creating the routers
        r1 = self.addHost('r1') 
        r2 = self.addHost('r2')
        r3 = self.addHost('r3')
        r4 = self.addHost('r4')
        
        #Creating the links between host and routers
        
        #Host A
        self.addLink(hostA, r1,
                    intfName1 = 'hostA-fa0', 
                    intfName2 = 'r1-fa0',
                    cls = TCLink,
                    bw=bw1) #network 1
        self.addLink(hostA, r2,
                    intfName1 = 'hostA-fa1', 
                    intfName2 = 'r2-fa0',
                    cls = TCLink,
                    bw=bw1) #network 2
        #Host B
        self.addLink(hostB, r3,
                    intfName1 = 'hostB-fa0', 
                    intfName2 = 'r3-fa0',
                    cls = TCLink,
                    bw=bw1) #network 7
        self.addLink(hostB, r4,
                    intfName1 = 'hostB-fa1',
                    intfName2 = 'r4-fa0',
                    cls = TCLink,
                    bw=bw1) #network 8
        
        #Creating the links between routers
        
        #Network 3
        self.addLink(r1, r3, intfName1='r1-se2', intfName2='r3-se2', cls = TCLink, bw=bw2)
        #Network 5
        self.addLink(r1, r4, intfName1='r1-se3', intfName2='r4-se3', cls = TCLink, bw=bw1)
        
        #Network 4
        self.addLink(r2, r4, intfName1='r2-se2', intfName2='r4-se2', cls = TCLink, bw=bw2)
        #Network 6
        self.addLink(r2, r3, intfName1='r2-se3', intfName2='r3-se3', cls = TCLink, bw=bw1)

def assign_IP(h1,h2,r1,r2,r3,r4):
    '''Assign IP addresses to the hosts & routers'''

    #Configure IP addresses for hosts

    #define NIC for hostA
    h1.cmd('ifcongfig hostA-fa0 0')
    h1.cmd('ifcongfig hostA-fa1 0')
    #define IP address for hostA interfaces
    h1.cmd('ifconfig hostA-fa0 192.168.1.1 netmask 255.255.255.252') #network 1
    h1.cmd('ifconfig hostA-fa1 192.168.1.5 netmask 255.255.255.252') #network 2

    #define NIC for hostB
    h2.cmd('ifcongfig hostB-fa0 0')
    h2.cmd('ifcongfig hostB-fa1 0')
    #define IP address for hostB interfaces
    h2.cmd('ifconfig hostB-fa0 192.168.1.25 netmask 255.255.255.252') #network 7
    h2.cmd('ifconfig hostB-fa1 192.168.1.29 netmask 255.255.255.252') #network 8

    #Enabling routers IP Forwarding for hosts
    # r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    # r2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    # r3.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    # r4.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')

    #Configure IP addresses for routers
    
    #define NIC for r1
    r1.cmd('ifcongfig r1-fa0 0')
    r1.cmd('ifcongfig r1-se2 0')
    r1.cmd('ifcongfig r1-se3 0')
    #define IP address for r1 interfaces
    r1.cmd('ifconfig r1-fa0 192.168.1.2 netmask 255.255.255.252') #network 1
    r1.cmd('ifconfig r1-se2 192.168.1.9 netmask 255.255.255.252') #network 3
    r1.cmd('ifconfig r1-se3 192.168.1.17 netmask 255.255.255.252') #network 5

    #define NIC for r2
    r2.cmd('ifcongfig r2-fa0 0')
    r2.cmd('ifcongfig r2-se2 0')
    r2.cmd('ifcongfig r2-se3 0')
    #define IP address for r2 interfaces
    r2.cmd('ifconfig r2-fa0 192.168.1.6 netmask 255.255.255.252') #network 2
    r2.cmd('ifconfig r2-se2 192.168.1.13 netmask 255.255.255.252') #network 4
    r2.cmd('ifconfig r2-se3 192.168.1.21 netmask 255.255.255.252') #network 6

    #define NIC for r3
    r3.cmd('ifcongfig r3-fa0 0')
    r3.cmd('ifcongfig r3-se2 0')
    r3.cmd('ifcongfig r3-se3 0')
    #define IP address for r3 interfaces
    r3.cmd('ifconfig r3-fa0 192.168.1.26 netmask 255.255.255.252') #network 7
    r3.cmd('ifconfig r3-se2 192.168.1.10 netmask 255.255.255.252') #network 3
    r3.cmd('ifconfig r3-se3 192.168.1.22 netmask 255.255.255.252') #network 6

    #define NIC for r4
    r4.cmd('ifcongfig r4-fa0 0')
    r4.cmd('ifcongfig r4-se2 0')
    r4.cmd('ifcongfig r4-se3 0')
    #define IP address for r4 interfaces
    r4.cmd('ifconfig r4-fa0 192.168.1.30 netmask 255.255.255.252') #network 8
    r4.cmd('ifconfig r4-se2 192.168.1.14 netmask 255.255.255.252') #network 4
    r4.cmd('ifconfig r4-se3 192.168.1.18 netmask 255.255.255.252') #network 5

def static_routing(h1,h2,r1,r2,r3,r4):
    '''Configure static routing for each nodes'''

    #Neighbors routing for each nodes

    #Configure static routing for hostA
    h1.cmd('ip rule add from 192.168.1.1 table 1') #network 1
    h1.cmd('ip rule add from 192.168.1.5 table 2') #network 2
    #network 1
    h1.cmd('ip route add 192.168.1.0/30 dev hostA-fa0 scope link table 1')
    h1.cmd('ip route add default via 192.168.1.2 dev hostA-fa0 table 1')
    #network 2
    h1.cmd('ip route add 192.168.1.4/30 dev hostA-fa1 scope link table 2')
    h1.cmd('ip route add default via 192.168.1.6 dev hostA-fa1 table 2')
    #add default route for hostA
    h1.cmd('ip route add default scope global nexthop via 192.168.1.2 dev hostA-fa0')

    #Configure static routing for hostB
    h2.cmd('ip rule add from 192.168.1.25 table 1') #network 7
    h2.cmd('ip rule add from 192.168.1.29 table 2') #network 8
    #network 7
    h2.cmd('ip route add 192.168.1.24/30 dev hostB-fa0 scope link table 1')
    h2.cmd('ip route add default via 192.168.1.26 dev hostB-fa0 table 1')
    #network 8
    h2.cmd('ip route add 192.168.1.28/30 dev hostB-fa1 scope link table 2')
    h2.cmd('ip route add default via 192.168.1.30 dev hostB-fa1 table 2')
    #add default route for hostB
    h2.cmd('ip route add default scope global nexthop via 192.168.1.26 dev hostB-fa0')

    #Configure static routing for routers

    #r1
    r1.cmd('ip rule add from 192.168.1.2 table 1') #network 1
    r1.cmd('ip rule add from 192.168.1.9 table 2') #network 3
    r1.cmd('ip rule add from 192.168.1.17 table 3') #network 5
    #network 1
    r1.cmd('ip route add 192.168.1.0/30 dev r1-fa0 scope link table 1')
    r1.cmd('ip route add default via 192.168.1.1 dev r1-fa0 table 1')
    #network 3
    r1.cmd('ip route add 192.168.1.8/30 dev r1-se2 scope link table 2')
    r1.cmd('ip route add default via 192.168.1.10 dev r1-se2 table 2')
    #network 5
    r1.cmd('ip route add 192.168.1.16/30 dev r1-se3 scope link table 3')
    r1.cmd('ip route add default via 192.168.1.18 dev r1-se3 table 3')
    #add default route for r1
    r1.cmd('ip route add default scope global nexthop via 192.168.1.1 dev r1-fa0')

    #r2
    r2.cmd('ip rule add from 192.168.1.6 table 1') #network 2
    r2.cmd('ip rule add from 192.168.1.13 table 2') #network 4
    r2.cmd('ip rule add from 192.168.1.21 table 3') #network 6
    #network 2
    r2.cmd('ip route add 192.168.1.4/30 dev r2-fa0 scope link table 1')
    r2.cmd('ip route add default via 192.168.1.5 dev r2-fa0 table 1')
    #network 4
    r2.cmd('ip route add 192.168.1.12/30 dev r2-se2 scope link table 2')
    r2.cmd('ip route add default via 192.168.1.14 dev r2-se2 table 2')
    #network 6
    r2.cmd('ip route add 192.168.1.20/30 dev r2-se3 scope link table 3')
    r2.cmd('ip route add default via 192.168.1.22 dev r2-se3 table 3')
    #add default route for r2
    r2.cmd('ip route add default scope global nexthop via 192.168.1.5 dev r2-fa0')

    #r3
    r3.cmd('ip rule add from 192.168.1.26 table 1') #network 7
    r3.cmd('ip rule add from 192.168.1.10 table 2') #network 3
    r3.cmd('ip rule add from 192.168.1.22 table 3') #network 6
    #network 7
    r3.cmd('ip route add 192.168.1.24/30 dev r3-fa0 scope link table 1')
    r3.cmd('ip route add default via 192.168.1.25 dev r3-fa0 table 1')
    #network 3
    r3.cmd('ip route add 192.168.1.8/30 dev r3-se2 scope link table 2')
    r3.cmd('ip route add default via 192.168.1.9 dev r3-se2 table 2')
    #network 6
    r3.cmd('ip route add 192.168.1.22/30 dev r3-se3 scope link table 3')
    r3.cmd('ip route add default via 192.168.1.21 dev r3-se3 table 3')
    #add default route for r3
    r3.cmd('ip route add default scope global nexthop via 192.168.1.25 dev r3-fa0')

    #r4
    r4.cmd('ip rule add from 192.168.1.30 table 1') #network 8
    r4.cmd('ip rule add from 192.168.1.14 table 2') #network 4
    r4.cmd('ip rule add from 192.168.1.18 table 3') #network 5
    #network 8
    r4.cmd('ip route add 192.168.1.28/30 dev r4-fa0 scope link table 1')
    r4.cmd('ip route add default via 192.168.1.29 dev r4-fa0 table 1')
    #network 4
    r4.cmd('ip route add 192.168.1.12/30 dev r4-se2 scope link table 2')
    r4.cmd('ip route add default via 192.168.1.13 dev r4-se2 table 2')
    #network 5
    r4.cmd('ip route add 192.168.1.16/30 dev r4-se3 scope link table 3')
    r4.cmd('ip route add default via 192.168.1.17 dev r4-se3 table 3')
    #add default route for r4
    r4.cmd('ip route add default scope global nexthop via 192.168.1.29 dev r4-fa0')

    #Setting up gateway for router r1 (exclude network 1,3,5)
    #Connecting network 2
    # r1.cmd('route add -net 192.168.1.4/30 gw 192.168.1.18') # via network 5
    # r1.cmd('route add -net 192.168.1.4/30 gw 192.168.1.10') # via network 3
    #Connecting network 4
    r1.cmd('route add -net 192.168.1.12/30 gw 192.168.1.18') # via network 5
    #Connecting network 6
    r1.cmd('route add -net 192.168.1.20/30 gw 192.168.1.10') # via network 3
    #Connecting network 7
    r1.cmd('route add -net 192.168.1.24/30 gw 192.168.1.10') #via network 3
    #Connecting network 8
    r1.cmd('route add -net 192.168.1.28/30 gw 192.168.1.18') #via network 5

    #Setting up gateway for router r2 (exclude network 2,4,6)
    #Connecting network 1
    # r2.cmd('route add -net 192.168.1.0/30 gw 192.168.1.22') #via network 6
    # r2.cmd('route add -net 192.168.1.0/30 gw 192.168.1.14') #via network 4
    #Connecting network 3
    r2.cmd('route add -net 192.168.1.8/30 gw 192.168.1.22') #via network 6
    #Connecting network 5
    r2.cmd('route add -net 192.168.1.16/30 gw 192.168.1.14') #via network 4
    #Connecting network 7
    r2.cmd('route add -net 192.168.1.24/30 gw 192.168.1.22') #via network 6
    #Connecting network 8
    r2.cmd('route add -net 192.168.1.28/30 gw 192.168.1.14') #via network 4

    #Setting up gateway for router r3 (exclude network 7,3,6)
    #Connecting network 1
    r3.cmd('route add -net 192.168.1.0/30 gw 192.168.1.9') #via network 3
    #Connecting network 2
    r3.cmd('route add -net 192.168.1.4/30 gw 192.168.1.21') #via network 6
    #Connecting network 4
    r3.cmd('route add -net 192.168.1.12/30 gw 192.168.1.21') #via network 6
    #Connecting network 5
    r3.cmd('route add -net 192.168.1.16/30 gw 192.168.1.9') #via network 3
    #Connecting network 8
    # r3.cmd('route add -net 192.168.1.28/30 gw 192.168.1.21') #via network 6
    # r3.cmd('route add -net 192.168.1.28/30 gw 192.168.1.9') #via network 3

    #Setting up gateway for router r4 (exclude network 8,4,5)
    #Connecting network 1
    r4.cmd('route add -net 192.168.1.0/30 gw 192.168.1.17') #via network 5
    #Connecting network 2
    r4.cmd('route add -net 192.168.1.4/30 gw 192.168.1.13') #via network 4
    #Connecting network 3
    r4.cmd('route add -net 192.168.1.8/30 gw 192.168.1.17') #via network 5
    #Connecting network 6
    r4.cmd('route add -net 192.168.1.20/30 gw 192.168.1.13') #via network 4
    #Connecting network 7
    # r4.cmd('route add -net 192.168.1.24/30 gw 192.168.1.13') #via network 4
    # r4.cmd('route add -net 192.168.1.24/30 gw 192.168.1.17') #via network 5

def test_ping(h1, h2, r1, r2, r3, r4):
    # Ping test for CLO 1
    info('*** Testing ping between hosts\n')
    h1.cmdPrint('ping -c1 192.168.1.2') #hostA ping r1 (network 1)
    h1.cmdPrint('ping -c1 192.168.1.6') #hostA ping r2 (network 2)
    h1.cmdPrint('ping -c1 192.168.1.10') #hostA ping r3
    h1.cmdPrint('ping -c1 192.168.1.14') #hostA ping r4

    h2.cmdPrint('ping -c1 192.168.1.9') #hostB ping r1
    h2.cmdPrint('ping -c1 192.168.1.13') #hostB ping r2
    h2.cmdPrint('ping -c1 192.168.1.26') #hostB ping r3 (network 7)
    h2.cmdPrint('ping -c1 192.168.1.30') #hostB ping r4 (network 8)

    r1.cmdPrint('ping -c1 192.168.1.21') #r1 ping r2
    r1.cmdPrint('ping -c1 192.168.1.10') #r1 ping r3 (network 3)
    r1.cmdPrint('ping -c1 192.168.1.18') #r1 ping r4 (network 5)

    r2.cmdPrint('ping -c1 192.168.1.22') #r2 ping r3 (network 5)
    r2.cmdPrint('ping -c1 192.168.1.9') #r2 ping r1

    r3.cmdPrint('ping -c1 192.168.1.14') #r3 ping r4

def runTopo():
    '''Bootstrap a Mininet network using the Minimal Topology'''
    os.system('mn -cc')
    key = 'net.mptcp.enabled'
    value = 1
    p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print("stdout=",stdout,"stderr=",stderr)

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    
    #Build the network based on topology
    net.start()
    #Put object into variables for easy access
    h1,h2,r1,r2,r3,r4 = net.get('hostA','hostB','r1','r2','r3','r4')
    #Assign IP addresses to the hosts & routers
    assign_IP(h1,h2,r1,r2,r3,r4)
    static_routing(h1,h2,r1,r2,r3,r4)
    
    #test ping
    # test_ping(h1,h2,r1,r2,r3,r4)
    # info('\n', net.pingAll(), '\n')
    
    CLI(net)
    net.stop()



if __name__=='__main__':
    setLogLevel('info')
    runTopo()