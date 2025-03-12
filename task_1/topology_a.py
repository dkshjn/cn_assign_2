from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController

class CustomTopo(Topo):
    def build(self):
        # Add switches
        s1, s2, s3, s4 = [self.addSwitch(f's{i}') for i in range(1, 5)]

        # Add hosts
        h1, h2 = self.addHost('h1'), self.addHost('h2')
        h3, h4 = self.addHost('h3'), self.addHost('h4')
        h5, h6 = self.addHost('h5'), self.addHost('h6')
        h7 = self.addHost('h7')  # TCP Server

        # Connect hosts to switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s3)
        self.addLink(h5, s2)
        self.addLink(h6, s3)
        self.addLink(h7, s4)  # Server connected to switch 4

        # Connect switches
        self.addLink(s1, s4)
        self.addLink(s2, s4)
        self.addLink(s3, s4)

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=None)  # No default controller
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)  # Connect to POX or Ryu

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
