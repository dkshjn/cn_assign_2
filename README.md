# Computer Networks (CS-331) - Assignment 2

## Authors
Daksh Jain (22110066), Harshit (22110095)

## Task 1


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
