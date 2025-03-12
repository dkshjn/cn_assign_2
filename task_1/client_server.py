import argparse
import time
import os
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def parse_args():
    parser = argparse.ArgumentParser(description="Mininet TCP Congestion Control Experiment")
    parser.add_argument("--option", choices=['a', 'b', 'c', 'd'], required=True, help="Experiment part: a, b, c, or d")
    parser.add_argument("--cc", choices=['cubic', 'westwood', 'scalable'], required=True, help="Congestion control algorithm")
    return parser.parse_args()

class CustomTopo(Topo):
    def build(self):
        # Final topology from Part (a)
        s1, s2, s3, s4 = [self.addSwitch(f's{i}') for i in range(1, 5)]
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
        self.addLink(h7, s4)
        
        # Connect switches with final topology
        self.addLink(s1, s4)
        self.addLink(s2, s4)
        self.addLink(s3, s4)

def run_experiment(option, cc):
    log_dir = f"/tmp/part_{option}/{cc}/"
    os.system(f"mkdir -p {log_dir}")

    topo = CustomTopo()
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.start()

    h7 = net.get('h7')
    clients = {'h1': net.get('h1'), 'h3': net.get('h3'), 'h4': net.get('h4')}
    
    # Configure loss if Part (d)
    if option == 'd':
        for loss_rate in [1, 5]:
            print(f"Applying {loss_rate}% packet loss on S2-S3")
            net.get('s2').cmd(f'tc qdisc add dev s2-eth2 root netem loss {loss_rate}%')
    
    print(f"Starting TCP server on H7 ({cc})...")
    h7.cmd(f'iperf3 -s -p 5001 > {log_dir}h7_server.log &')
    h7.cmd(f'tcpdump -i h7-eth0 -w {log_dir}h7_capture.pcap &')
    time.sleep(2)
    
    # Start experiments based on option
    if option == 'a':
        clients['h1'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 30 -C {cc} -J > {log_dir}h1_{cc}.json &')
    elif option == 'b':
        clients['h1'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 150 -C {cc} -J > {log_dir}h1_{cc}.json &')
        time.sleep(15)
        clients['h3'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 120 -C {cc} -J > {log_dir}h3_{cc}.json &')
        time.sleep(15)
        clients['h4'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 90 -C {cc} -J > {log_dir}h4_{cc}.json &')
    elif option == 'c' or option == 'd':
        clients['h1'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 150 -C {cc} -J > {log_dir}h1_{cc}.json &')
        clients['h3'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 150 -C {cc} -J > {log_dir}h3_{cc}.json &')
        clients['h4'].cmd(f'iperf3 -c 10.0.0.7 -p 5001 -t 150 -C {cc} -J > {log_dir}h4_{cc}.json &')
    
    time.sleep(150)
    print("Stopping Wireshark capture...")
    h7.cmd('pkill tcpdump')
    
    print(f"Experiment {option} with {cc} complete! Logs stored in {log_dir}.")
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    args = parse_args()
    run_experiment(args.option, args.cc)

