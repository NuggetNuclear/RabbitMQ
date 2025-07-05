import pika, time, os, sys

# Salida sin buffer
sys.stdout.reconfigure(line_buffering=True)

# Parámetros por variables de entorno
RABBITMQ_HOST = os.getenv("BROKER_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("BROKER_PORT", 5672))
RABBITMQ_USER = os.getenv("BROKER_USER", "gabriel")
RABBITMQ_PASS = os.getenv("BROKER_PASS", "insaid33")
QUEUE        = os.getenv("QUEUE",        "Cola_Mensajes")

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

def cerrar(motivo=""):
    print(f"\n[FIN] Conexión cerrada: {motivo}", flush=True)
    try:
        chan.close()
        conn.close()
    finally:
        sys.exit(0)

def callback(ch, method, props, body):
    txt = body.decode(errors="ignore")
    if "hackeado" in txt.lower():
        print("🛑  MENSAJE HACKEADO DETECTADO → cerrando conexión")
        cerrar("Mensaje hackeado")
    else:
        print(f"[MSG] {txt}")

chan.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
try:
    chan.start_consuming()
except KeyboardInterrupt:
    cerrar("Interrupción usuario")
except Exception as e:
    cerrar(str(e))
