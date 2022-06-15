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
        hostA = self.addHost('hostA', ip='192.168.1.10/24')
        hostB = self.addHost('hostB', ip='192.168.1.20/24')
        
        #Creating the routers
        r1 = self.addHost('r1', ip='192.168.255.1/30') 
        r2 = self.addHost('r2', ip='192.168.255.2/30')
        r3 = self.addHost('r3', ip='192.168.255.5/30')
        r4 = self.addHost('r4', ip='192.168.255.6/30')
        
        #Creating the switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        #Creating the links between host and switch
        self.addLink(hostA, s1,intfName1='s1-eth1') #network A (192.168.255.0/24)
        self.addLink(hostB, s2,intfName1='s2-eth1') #network B (192.168.255.4/24)
        #Creating the links between switch and routers
        self.addLink(s1, r1, intfName1='r1-eth0', intfName2='s1-eth1', bw=bw1)
        self.addLink(s1, r2, intfName1='r2-eth0', intfName2='s2-eth1', bw=bw1)
        self.addLink(s2, r3, intfName1='r3-eth0', intfName2='s2-eth1', bw=bw1)
        self.addLink(s2, r4, intfName1='r4-eth0', intfName2='s1-eth1', bw=bw1)
        #Creating the links between routers
        self.addLink(r1, r3, intfName1='r1-eth1', intfName2='r3-eth1', bw=bw2)
        self.addLink(r2, r4, intfName1='r2-eth1', intfName2='r4-eth1', bw=bw2)
        self.addLink(r1, r4, intfName1='r1-eth2', intfName2='r4-eth2', bw=bw1)
        self.addLink(r2, r3, intfName1='r2-eth2', intfName2='r3-eth2', bw=bw1)

def runTopo():
    '''Bootstrap a Mininet network using the Minimal Topology'''
    os.system('mn -cc')

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()

    #Put object into variables for easy access
    h1,h2,r1,r2,r3,r4,s1,s2 = net.get('hostA','hostB','r1','r2','r3','r4','s1','s2')
    
    #Ping All
    info('\n', net.ping(), '\n')

if __name__=='__main__':
    setLogLevel('info')
    runTopo()