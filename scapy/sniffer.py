from scapy.all import sniff, get_if_list, wrpcap

# Elegir interfaz
interfaces = get_if_list()
print("Interfaces detectadas:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("Elige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (
    interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str
)

FILTER = "tcp port 5672"
OUTPUT = "/captures/trace.pcap"

print(f"Sniffing AMQP en interfaz {IFACE} (filtro: {FILTER})")
capturados = sniff(filter=FILTER, iface=IFACE, prn=lambda pkt: print(pkt.summary()), store=1)
wrpcap(OUTPUT, capturados)
print(f"\nGuardado {len(capturados)} paquetes en {OUTPUT}", flush=True)
