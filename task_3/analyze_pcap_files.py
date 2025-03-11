import subprocess
import sys

# Get statistics from PCAP file.
def get_capture_summary(pcap_file):
    cmd = f"tshark -r {pcap_file} -q -z io,stat,100"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    lines = result.stdout.split("\n")
    total_bytes = None
    time_span = None

    for line in lines:
        if "|   " in line and " | " in line:
            parts = line.split("|")
            total_bytes = int(parts[3].strip())
            time_span = float(parts[2].strip())

    return total_bytes, time_span

def get_retransmissions(pcap_file):
    cmd = f"tshark -r {pcap_file} -Y 'tcp.analysis.retransmission' | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return int(result.stdout.strip())

def get_total_packets(pcap_file):
    cmd = f"tshark -r {pcap_file} | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return int(result.stdout.strip())

def get_max_packet_size(pcap_file):
    cmd = f"tshark -r {pcap_file} -T fields -e frame.len"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    packet_sizes = [int(x) for x in result.stdout.split() if x.isdigit()]
    
    return max(packet_sizes) if packet_sizes else 0

def analyze_pcap(pcap_file):
    print(f"\nAnalyzing PCAP file: {pcap_file}...\n")
    
    total_bytes, time_span = get_capture_summary(pcap_file)
    if total_bytes is None or time_span is None:
        print("Error.")
        return
    
    # Throughput
    throughput = total_bytes / time_span if time_span > 0 else 0
    
    # Retransmissions
    retransmissions = get_retransmissions(pcap_file)
    
    # Goodput
    goodput = (total_bytes - (retransmissions * 40)) / time_span if time_span > 0 else 0
    
    # Total packets
    total_packets = get_total_packets(pcap_file)
    
    # Packet Loss Rate
    packet_loss_rate = (retransmissions / total_packets) * 100 if total_packets > 0 else 0
    
    # Max packet size
    max_packet_size = get_max_packet_size(pcap_file)
    
    print(f"Results for {pcap_file}:")
    print(f"Throughput: {throughput:.2f} Bytes/sec")
    print(f"Goodput: {goodput:.2f} Bytes/sec")
    print(f"Packet Loss Rate: {packet_loss_rate:.2f}%")
    print(f"Maximum Packet Size: {max_packet_size} Bytes\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    for pcap in sys.argv[1:]:
        analyze_pcap(pcap)
