import pika, time, os, sys

# Salida sin buffer
sys.stdout.reconfigure(line_buffering=True)

# Parámetros por variables de entorno
RABBITMQ_HOST = os.getenv("BROKER_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("BROKER_PORT", 5672))
RABBITMQ_USER = os.getenv("BROKER_USER", "gabriel")
RABBITMQ_PASS = os.getenv("BROKER_PASS", "insaid33")
QUEUE = os.getenv("QUEUE", "Cola_Mensajes")

param = pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host="/",
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
)

# Conexión con reintentos
for i in range(20):
    try:
        conn = pika.BlockingConnection(param)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[ESPERA] Rabbit no listo ({i+1}/20)…")
        time.sleep(3)
else:
    sys.exit("No se pudo conectar.")

chan = conn.channel()
chan.queue_declare(queue=QUEUE, durable=False)
print(f"[RECEPTOR] Escuchando en «{QUEUE}»\n")

def callback(ch, method, props, body):
    txt = body.decode(errors="ignore")
    print(f"[MSG] {txt}")

chan.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
try:
    chan.start_consuming()
except KeyboardInterrupt:
    print("\n[FIN] Interrupción usuario", flush=True)
    chan.close()
    conn.close()
except Exception as e:
    print(f"\n[FIN] Error: {e}", flush=True)
    chan.close()
    conn.close()