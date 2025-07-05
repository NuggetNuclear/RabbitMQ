from scapy.all import *
import argparse
import os

def elegir_interfaz():
    ifaces = get_if_list()
    print("Interfaces de red disponibles:")
    for i, iface in enumerate(ifaces):
        print(f"  [{i}] {iface}")
    while True:
        sel = input("Selecciona el número de la interfaz a snifar: ")
        try:
            num = int(sel)
            if 0 <= num < len(ifaces):
                return ifaces[num]
        except:
            pass
        print("Selección inválida, intenta de nuevo.")

parser = argparse.ArgumentParser(description="Sniffer AMQP simple")
parser.add_argument("--iface", "-i", default=None,
                    help="Interfaz de red a esnifar (ej: eth0, lo, docker0, etc)")
parser.add_argument("--timeout", "-t", type=int, default=60,
                    help="Segundos a capturar (default: 60)")
args = parser.parse_args()

# Selección interactiva si no se da --iface
iface = args.iface if args.iface else elegir_interfaz()

# Crea el directorio de captura si no existe
os.makedirs("/captura", exist_ok=True)
pcap_path = "/captura/captura_amqp.pcap"

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

print(f"Sniffeando AMQP en TCP 5672, interfaz: {iface} ({args.timeout} segundos)")
sniff(filter="tcp port 5672",
      iface=iface,
      prn=mostrar_paquete,
      store=0,
      timeout=args.timeout)

wrpcap(pcap_path, capturados)
print(f"Captura guardada en {pcap_path}")