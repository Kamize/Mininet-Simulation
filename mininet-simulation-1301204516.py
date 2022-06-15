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
                    intfName2 = 'r4-fa1'
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
    

    # net.start()
    #Ping All
    #info('\n', net.ping(), '\n')

    

if __name__=='__main__':
    setLogLevel('info')
    runTopo()