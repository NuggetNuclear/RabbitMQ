from scapy.all import sniff, TCP, Raw, wrpcap
import argparse

parser = argparse.ArgumentParser(description="Sniffer AMQP simple")
parser.add_argument("--iface", "-i", default=None,
                    help="Interfaz de red a esnifar (ej: eth0, lo, docker0, etc)")
parser.add_argument("--timeout", "-t", type=int, default=60,
                    help="Segundos a capturar (default: 60)")
args = parser.parse_args()

capturados = []

def mostrar_paquete(pkt):
    if pkt.haslayer(Raw):
        data = pkt[Raw].load
        try:
            texto = data.decode(errors="ignore").strip()
            if texto:
                print(texto)
        except Exception:
            pass
        capturados.append(pkt)

print(f"Sniffeando AMQP en TCP 5672, interfaz: {args.iface or 'todas'} ({args.timeout} segundos)")
sniff(filter="tcp port 5672",
      iface=args.iface,
      prn=mostrar_paquete,
      store=0,
      timeout=args.timeout)

wrpcap("captura_amqp.pcap", capturados)
print("Captura guardada en captura_amqp.pcap")