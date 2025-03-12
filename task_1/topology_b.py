from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import subprocess

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

def start_experiment():
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=None)  # No default controller
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)  # Connect to POX or Ryu

    net.start()
    
    # Get host objects
    h1, h3, h4, h7 = net.get('h1', 'h3', 'h4', 'h7')

    print("Starting TCP server on H7...")
    h7.cmd('iperf3 -s -p 5001 > /tmp/h7_server.log &')

    print("Starting Wireshark capture on H7...")
    h7.cmd('tcpdump -i h7-eth0 -w /tmp/h7_capture.pcap &')

    time.sleep(2)  # Wait for the server to initialize

    # Run clients at staggered times
    print("Starting H1 client at T=0s...")
    h1.cmd('iperf3 -c 10.0.0.7 -p 5001 -b 10M -P 10 -t 150 -C cubic -J > /tmp/h1_scalable.json &')

    time.sleep(15)  # Wait 15 seconds

    print("Starting H3 client at T=15s...")
    h3.cmd('iperf3 -c 10.0.0.7 -p 5001 -b 10M -P 10 -t 120 -C cubic -J > /tmp/h3_scalable.json &')

    time.sleep(15)  # Wait another 15 seconds

    print("Starting H4 client at T=30s...")
    h4.cmd('iperf3 -c 10.0.0.7 -p 5001 -b 10M -P 10 -t 90 -C cubic -J > /tmp/h4_scalable.json &')

    # Wait for experiment to finish
    time.sleep(150)

    print("Stopping Wireshark capture...")
    h7.cmd('pkill tshark')

    print("Experiment complete! Logs stored in /tmp/.")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_experiment()

