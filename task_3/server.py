import socket

HOST = '0.0.0.0'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nagle = input("Enable Nagle's Algorithm? (yes/no): ").strip().lower()
if nagle == "no":
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[*] Server listening on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"[+] Connected to {addr}")

delayed_ack = input("Enable Delayed-ACK? (yes/no): ").strip().lower()
if delayed_ack == "no":
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

received_data = b""
while len(received_data) < 4096:
    data = conn.recv(40)
    if not data:
        break
    received_data += data
    print(f"Received {len(received_data)}/{4096} bytes")

print("[*] File received. Now, closing connection.")
conn.close()
server_socket.close()
