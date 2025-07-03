# sender_cli.py
import pika, sys, time, argparse

parser = argparse.ArgumentParser(
    description="CLI sender pa' Rabbit – full control de frecuencia y mensaje"
)
parser.add_argument("--freq", "-f", type=float, default=1.0,
                    help="Segundos entre mensajes (default 1.0)")
parser.add_argument("--msg", "-m", default="Hello",
                    help="Texto base del mensaje (default 'Hello')")
parser.add_argument("--interactive", "-i", action="store_true",
                    help="Modo interactivo: leyéndote línea a línea de stdin")
args = parser.parse_args()

# –– 20 intentos de conexión, 3 s c/u (ya estaba en tu script original) –– :contentReference[oaicite:0]{index=0}
params = pika.ConnectionParameters(
    "rabbitmq", 5672, "/", pika.PlainCredentials("gabriel", "insaid33")
)
for i in range(20):
    try:
        conn = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[WAIT] RabbitMQ no ready, retry {i+1}/20…", flush=True)
        time.sleep(3)
else:
    sys.exit("😭 No se pudo conectar luego de 20 reintentos")

ch = conn.channel()
ch.queue_declare(queue="holas", durable=True)

def send(body):
    ch.basic_publish(
        exchange="",
        routing_key="holas",
        body=body.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"[SENDER] Sent: {body}", flush=True)

if args.interactive:
    print("🔮 Type & Enter (Ctrl-D = exit)")
    for line in sys.stdin:
        txt = line.rstrip("\n")
        if txt:
            send(txt)
else:
    n = 1
    try:
        while True:
            send(f"{args.msg} ({n})")
            n += 1
            time.sleep(args.freq)
    except KeyboardInterrupt:
        pass

conn.close()
print("👋 Bye !")
