#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from time import time
from mininet.util import pmonitor
from signal import SIGINT
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
        self.addlink(hostA, r2,
                    intfName1 = 'hostA-fa1', 
                    intfName2 = 'r2-fa1',
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
                    intfName2 = 'r4-fa1',
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

def runTopo():
    '''Bootstrap a Mininet network using the Minimal Topology'''
    os.system('mn -cc')

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    
    net.build()
    
    #Put object into variables for easy access
    h1,h2,r1,r2,r3,r4 = net.get('hostA','hostB','r1','r2','r3','r4')

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
    r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    r2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    r3.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    r4.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    
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
    
    # net.start()
    #Ping All
    #info('\n', net.ping(), '\n')



if __name__=='__main__':
    setLogLevel('info')
    runTopo()