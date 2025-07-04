import socket
import threading
from termcolor import cprint
import os

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 5672
BACKEND_HOST = os.environ.get("BACKEND_HOST", "rabbit")
BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 5672))

def handle(client, remote):
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            # Parchea aquí: ejemplo, reemplaza "Hola" por "Hacked"
            patched = data.replace(b"Hola", b"Hacked")
            remote.sendall(patched)
        except Exception as e:
            cprint(f"Error en handle(client→remote): {e}", "red")
            break
    client.close()
    remote.close()

def handle_back(remote, client):
    while True:
        try:
            data = remote.recv(4096)
            if not data:
                break
            client.sendall(data)
        except Exception as e:
            cprint(f"Error en handle(remote→client): {e}", "red")
            break
    remote.close()
    client.close()

def main():
    cprint(f"PROXY AMQP levantando en {LISTEN_HOST}:{LISTEN_PORT} → {BACKEND_HOST}:{BACKEND_PORT}", "magenta", attrs=["bold"])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(100)
    while True:
        client_sock, addr = server.accept()
        cprint(f"[NEW CONN] de {addr}", "yellow")
        # conecta al broker real
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((BACKEND_HOST, BACKEND_PORT))
        threading.Thread(target=handle, args=(client_sock, remote), daemon=True).start()
        threading.Thread(target=handle_back, args=(remote, client_sock), daemon=True).start()

if __name__ == "__main__":
    main()
