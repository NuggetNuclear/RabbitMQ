from scapy.all import sniff, TCP, Raw, wrpcap

capturados = []

def mostrar_paquete(pkt):
    if pkt.haslayer(Raw):
        data = pkt[Raw].load
        try:
            texto = data.decode(errors="ignore")
            texto_limpio = texto.strip()
            if texto_limpio:
                print(texto_limpio)
        except Exception:
            pass
        capturados.append(pkt)

print("Sniffeando paquetes AMQP en TCP 5672... Solo texto del mensaje.")
sniff(filter="tcp port 5672", prn=mostrar_paquete, store=0, timeout=60)

wrpcap("captura_amqp.pcap", capturados)
print("Captura guardada en captura_amqp.pcap")