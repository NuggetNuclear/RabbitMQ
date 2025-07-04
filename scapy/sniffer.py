from scapy.all import sniff, wrpcap, get_if_list

OUTPUT = "/captures/trace.pcap"

# Lista interfaces disponibles
interfaces = get_if_list()
print("Interfaces detectadas en este contenedor:")
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}")

# Pregunta interfaz (nombre o número)
input_str = input("\nElige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
if input_str == "":
    IFACE = "eth0"
elif input_str.isdigit() and 1 <= int(input_str) <= len(interfaces):
    IFACE = interfaces[int(input_str) - 1]
else:
    IFACE = input_str

FILTER = "tcp port 5672"
print(f"\nSniffing interface: {IFACE} | filter: {FILTER}")

pkts = sniff(filter=FILTER, iface=IFACE, timeout=60)
wrpcap(OUTPUT, pkts)
print(f"Guardado {len(pkts)} paquetes en {OUTPUT}")
