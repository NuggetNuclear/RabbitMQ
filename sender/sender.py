import pika, sys, time, argparse, os

parser = argparse.ArgumentParser(
    description="Enviador de mensajes RabbitMQ"
)
parser.add_argument("--frecuencia", "-f", type=float, default=1.0,
                    help="Segundos entre mensajes (por defecto 1.0)")
parser.add_argument("--mensaje", "-m", default="Hola",
                    help="Texto base del mensaje (por defecto 'Hola')")
parser.add_argument("--interactivo", "-i", action="store_true",
                    help="Modo interactivo: leer líneas desde la entrada estándar")
parser.add_argument("--cola", "-q", default=os.environ.get("QUEUE", "Cola_Mensajes"),
                    help="Nombre de la cola (default: Cola_Mensajes o $QUEUE)")
args = parser.parse_args()

print(f"[INICIO] Enviador de mensajes RabbitMQ (frecuencia={args.frecuencia}, mensaje='{args.mensaje}')", flush=True)

# Parámetros por env-var (default si no están)
RABBITMQ_HOST = os.environ.get("BROKER_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.environ.get("BROKER_PORT", 5672))
RABBITMQ_USER = os.environ.get("BROKER_USER", "gabriel")
RABBITMQ_PASS = os.environ.get("BROKER_PASS", "insaid33")

parametros = pika.ConnectionParameters(
    RABBITMQ_HOST, RABBITMQ_PORT, "/", pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
)
for intento in range(20):
    try:
        conexion = pika.BlockingConnection(parametros)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[ESPERA] RabbitMQ no está listo, reintento {intento+1}/20…", flush=True)
        time.sleep(3)
else:
    sys.exit("No se pudo conectar a RabbitMQ después de 20 intentos. Saliendo.")

canal = conexion.channel()
canal.queue_declare(queue=args.cola, durable=False)

def enviar(cuerpo):
    canal.basic_publish(
        exchange="",
        routing_key=args.cola,
        body=cuerpo.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"[EMISOR] Enviado: {cuerpo}", flush=True)

if args.interactivo:
    print("Escribe y presiona Enter para enviar (Ctrl-D = salir)", flush=True)
    try:
        for linea in sys.stdin:
            texto = linea.rstrip("\n")
            if texto:
                enviar(texto)
    except (EOFError, KeyboardInterrupt):
        print("\nModo interactivo finalizado.", flush=True)
else:
    n = 1
    try:
        while True:
            enviar(f"{args.mensaje} ({n})")
            n += 1
            time.sleep(args.frecuencia)
    except KeyboardInterrupt:
        pass

conexion.close()
print("Bye", flush=True)
