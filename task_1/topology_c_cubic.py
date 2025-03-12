from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import os

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

        # Connect switches with bandwidth constraints
        self.addLink(s1, s2, bw=100)  # 100 Mbps
        self.addLink(s2, s3, bw=50)   # 50 Mbps (bottleneck)
        self.addLink(s3, s4, bw=100)  # 100 Mbps

def run_experiment(exp_part, condition, clients, loss_rate=0):
    """Runs experiment for a specific condition of Part (c) or (d)."""
    log_dir = f"/tmp/part_{exp_part}/{condition}/"
    os.system(f"mkdir -p {log_dir}")  # Create directory for storing results

    topo = CustomTopo()
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    net.start()

    # Get host objects
    h7 = net.get('h7')
    client_hosts = [net.get(c) for c in clients]

    # Configure link loss if running Part (d)
    if exp_part == "d":
        print(f"Configuring {loss_rate}% packet loss on S2-S3...")
        net.get('s2').cmd(f'tc qdisc add dev s2-eth2 root netem loss {loss_rate}%')

    print(f"Starting TCP server on H7 (Part {exp_part}, {condition})...")
    h7.cmd(f'iperf3 -s -p 5001 > {log_dir}h7_server.log &')

    print(f"Starting Wireshark capture on H7 (Part {exp_part}, {condition})...")
    h7.cmd(f'tcpdump -i h7-eth0 -w {log_dir}h7_capture.pcap &')

    time.sleep(2)  # Wait for server to initialize

    # Start clients
    print(f"Running {condition} (Part {exp_part})")
    for client in client_hosts:
        client.cmd(f'iperf3 -c 10.0.0.7 -p 5001 -b 10M -P 10 -t 150 -C cubic -J > {log_dir}{client.name}_cubic.json &')

    time.sleep(150)  # Wait for experiment completion

    print(f"Stopping Wireshark capture (Part {exp_part}, {condition})...")
    h7.cmd('pkill tcpdump')

    print(f"Experiment for {condition} complete! Logs stored in {log_dir}.")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    # Part (c) - Different active links
    print("\n===== Running Part (c): No packet loss =====")
    run_experiment("c", "condition_1", ["h3"])               # Condition 1: H3 → H7 (S2-S4 active)
    run_experiment("c", "condition_2a", ["h1", "h2"])        # Condition 2a: H1, H2 → H7 (S1-S4 active)
    run_experiment("c", "condition_2b", ["h1", "h3"])        # Condition 2b: H1, H3 → H7 (S1-S4 active)
    run_experiment("c", "condition_2c", ["h1", "h3", "h4"])  # Condition 2c: H1, H3, H4 → H7 (S1-S4 active)

    # Part (d) - Packet loss experiments
    print("\n===== Running Part (d): 1% packet loss =====")
    run_experiment("d", "loss_1", ["h1", "h3", "h4"], loss_rate=1)

    print("\n===== Running Part (d): 5% packet loss =====")
    run_experiment("d", "loss_5", ["h1", "h3", "h4"], loss_rate=5)

