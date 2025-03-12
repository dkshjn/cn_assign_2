# Computer Networks (CS-331) - Assignment 2

## Authors
Daksh Jain (22110066), Harshit (22110095)

## Task 1

This repository contains the implementation and analysis of TCP congestion control algorithms using Mininet and a POX controller. The experiments evaluate different TCP congestion control mechanisms by measuring throughput, goodput, packet loss rate, and window size.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Running the Experiment](#running-the-experiment)
- [Data Extraction](#data-extraction)
- [Calculating Metrics](#calculating-metrics)

---

## Setup Instructions
### Install and Configure POX Controller
To use the POX controller, follow these steps:
```sh
# Clone the POX repository
git clone https://github.com/noxrepo/pox.git
cd pox
```
Start the POX controller in a separate terminal:
```sh
sudo python3 pox.py forwarding.l2_learning
```

---

## Running the Experiment
Each part of the experiment can be executed using the following steps.

1. **Run Mininet Topology:**
```sh
sudo python3 assignment_2.py --option <a|b|c|d> --cc <cubic|westwood|scalable>
```
2. **View Temporary Saved Files:**
```sh
ls -lh /tmp/
```
3. **Move Experiment Files Permanently:**
```sh
sudo mv /tmp/part_c /tmp/part_d ~<path_to_save>
```

---

## Data Extraction
Once the `.pcap` files are created, use the following commands to extract the necessary data.

### Calculate Total Data Sent
```sh
tshark -r h7_capture_cubic_150.pcap -Y "tcp && frame.time_relative <= 150" -T fields -e tcp.len | awk '{sum += $1} END {print sum}'
```

### Calculate Total Data Retransmitted
```sh
tshark -r h7_capture_cubic_150.pcap -Y "tcp.analysis.retransmission && frame.time_relative <= 150" -T fields -e tcp.len | awk '{sum += $1} END {print sum}'
```
### Calculate Maximum Window Size
To determine the maximum TCP window size from the `.pcap` file, use one of the following methods:

#### Method 1: Using Wireshark
1. Open Wireshark and load the `.pcap` file.
2. Navigate to **Statistics** > **IO Graphs**.
3. Set the Y-axis unit to **Window Scaling (tcp.window_size)**.
4. Identify the highest peak value in the graph, which represents the maximum window size.

#### Method 2: Using Tshark
```sh
tshark -r h7_capture_cubic_150.pcap -T fields -e tcp.window_size_value | sort -nr | head -1
```
This command sorts the window size values in descending order and returns the maximum window size recorded in the `.pcap` file.
---

## Calculating Metrics
The following formulas are used to compute throughput, goodput, and packet loss rate:

- **Throughput (Mbps)** = `(Total Bytes Transferred * 8) / (Time Duration * 10^6)`
- **Goodput (Mbps)** = `((Total Bytes Sent - Bytes Retransmitted) * 8) / (Time Duration * 10^6)`
- **Packet Loss Rate (%)** = `(Total Retransmitted Bytes / Total Sent Bytes) * 100`

**Example Calculation for Cubic:**
```sh
Throughput = (402577423 * 8) / (150 * 10^6) = 21.44 Mbps
Goodput = ((402577423 - 2960824) * 8) / (150 * 10^6) = 21.27 Mbps
Packet Loss Rate = (2960824 / 402577423) * 100 = 0.73%
```

---

## Task 2

### Part a

1. Open a terminal and start the server:
```sh
nc -l -p 8080
```

2. Open a second terminal and start capturing packets:
```sh
sudo tcpdump -i any port 8080 -w syn_flood.pcap
 ```

3. In a third terminal start the client:
```sh
nc 172.16.5.128 8080
```
**Note:**
* Send messages periodically for the first 20 seconds to simulate legitimate traffic.
* Continue sending messages throughout the experiment, from t=0 to t=140 seconds, including during the attack.


4. At **t=20** seconds, open a new terminal and start the SYN flood attack:

```sh
sudo hping3 -S --flood -p 8080 <server-ip>
```

5. At **t=120** seconds, stop the attack by pressing:
```sh
Ctrl + C
```

6. At **t=140** seconds, stop the client connection.

7. Stop the packet capture in the tcpdump terminal.
   
8. Run the analysis script to generate the plot:
```sh
python3 plot.py
```
This will plot connection duration vs. connection start time graph.

## Task 3

Run the server and client scripts, specifying yes/no to enable or disable Nagle’s Algorithm and Delayed-ACK on both the server and client sides.

1. Open a terminal and start the server:
   ```sh
   python3 server.py
   ```
2. Open a second terminal and start the client:
   ```sh
   python3 client.py
   ```
3. In a third terminal, start packet capture using tcpdump:
```sh
sudo tcpdump -i any port 12345 -w capture_y_y.pcap
```

4. Once all 4096 bytes have been sent, stop the capture by pressing Ctrl + C in the tcpdump terminal.

Repeat steps 1-4 for the remaining three configurations.

5. After obtaining all four ```.pcap files```, run the analysis script:
```sh
python3 analyze_pcap_files.py capture_y_y.pcap capture_y_n.pcap capture_n_y.pcap capture_n_n.pcap
```

This will output Throughput, Goodput, Packet Loss Rate, and Maximum Packet Size for each file.
