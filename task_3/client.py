import socket
import time

SERVER_IP = "127.0.0.1" 
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))


nagle = input("Enable Nagle's Algorithm? (yes/no): ").strip().lower()
if nagle == "no":
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

delayed_ack = input("Enable Delayed-ACK? (yes/no): ").strip().lower()
if delayed_ack == "no":
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

# file to be sent
file_data = b"A" * 4096
for i in range(0, len(file_data), 40):
    client_socket.send(file_data[i:i+40])
    time.sleep(1)
    print(f"Sent {i+40}/{4096} bytes")

print("[*] File sent.")
client_socket.close()
