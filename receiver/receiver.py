import pika
import time
import os
import sys

# Logs instantáneos
sys.stdout.reconfigure(line_buffering=True)

# Parámetros desde variables de entorno
RABBITMQ_HOST = os.environ.get("BROKER_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.environ.get("BROKER_PORT", 5672))
RABBITMQ_USER = os.environ.get("BROKER_USER", "gabriel")
RABBITMQ_PASS = os.environ.get("BROKER_PASS", "insaid33")
QUEUE = os.environ.get("QUEUE", "Cola_Mensajes")

parametros = pika.ConnectionParameters(
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    "/",
    pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
)

# –– 20 intentos de conexión, 3 s c/u  ––
for i in range(20):
    try:
        conexion = pika.BlockingConnection(parametros)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[ESPERA] RabbitMQ no está listo, reintento {i+1}/20…", flush=True)
        time.sleep(3)
else:
    sys.exit("No se pudo conectar a RabbitMQ después de 20 intentos. Saliendo.")

print("[RECEPTOR] Conectado a RabbitMQ", flush=True)
print("[RECEPTOR] Esperando mensajes en la cola:", QUEUE, flush=True)

canal = conexion.channel()
canal.queue_declare(queue=QUEUE, durable=False)

def callback(ch, method, properties, body):
    print(f"[RECEPTOR] Mensaje recibido: {body.decode()}", flush=True)
    print(f"  Delivery tag: {method.delivery_tag}", flush=True)
    print(f"  Exchange: {method.exchange}", flush=True)
    print(f"  Routing key: {method.routing_key}", flush=True)
    print(f"  Propiedades: {properties}", flush=True)
    print("", flush=True)

canal.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

try:
    canal.start_consuming()
except KeyboardInterrupt:
    print("\n[RECEPTOR] Finalizado por usuario.", flush=True)
    try:
        canal.close()
        conexion.close()
    except Exception:
        pass
