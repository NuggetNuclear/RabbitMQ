# amqp_sniffer.py
from scapy.all import sniff, get_if_list

# Pregunta interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

FILTER = "tcp port 5672"
print(f"Sniffing AMQP en interfaz {IFACE} (filtro: {FILTER})")
sniff(filter=FILTER, iface=IFACE, prn=lambda pkt: print(pkt.summary()), store=0)
