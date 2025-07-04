from scapy.all import sniff, wrpcap, get_if_list
from termcolor import cprint

OUTPUT = "/captures/trace.pcap"

interfaces = get_if_list()
cprint("Interfaces detectadas en este contenedor:", "cyan", attrs=["bold"])
for i, iface in enumerate(interfaces):
    cprint(f"  [{i+1}] {iface}", "yellow")

input_str = input(f"\n¿Elige la interfaz por nombre o número (ENTER para 'eth0')? ").strip()
if input_str == "":
    IFACE = "eth0"
elif input_str.isdigit() and 1 <= int(input_str) <= len(interfaces):
    IFACE = interfaces[int(input_str) - 1]
else:
    IFACE = input_str

FILTER = "tcp port 5672"
cprint(f"\nSniffing interface: {IFACE} | filter: {FILTER}\n", "cyan")

pkts = sniff(filter=FILTER, iface=IFACE, timeout=60)
wrpcap(OUTPUT, pkts)
cprint(f"Saved {len(pkts)} packets to {OUTPUT}", "green", attrs=["bold"])
