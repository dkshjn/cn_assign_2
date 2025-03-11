# Computer Networks (CS-331) - Assignment 2

## Authors
Daksh Jain (22110066), Harshit (22110095)

## Task 1


## Task 2


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
