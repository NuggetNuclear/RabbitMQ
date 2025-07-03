import pika
import time
import sys; sys.stdout.reconfigure(line_buffering=True)

parameters = pika.ConnectionParameters(
    'rabbitmq', 5672, '/', pika.PlainCredentials('gabriel', 'insaid33')
)

# 💥 Intentar conectar con retry (máximo 20 intentos, espera 3s entre cada uno)
for i in range(20):
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[WAIT] RabbitMQ not ready yet, retrying in 3s... ({i+1}/20)")
        time.sleep(3)
else:
    raise Exception("No se pudo conectar a RabbitMQ luego de 20 intentos :(")

channel = connection.channel()
channel.queue_declare(queue='holas')

def callback(ch, method, properties, body):
    print(f"[RECEIVER] Got: {body.decode()}")
    print(f"  Delivery tag: {method.delivery_tag}")
    print(f"  Exchange: {method.exchange}")
    print(f"  Routing key: {method.routing_key}")
    print(f"  Properties: {properties}")
    print("")

channel.basic_consume(queue='holas', on_message_callback=callback, auto_ack=True)

print("[RECEIVER] Esperando mensajes (Ctrl+C para salir)...")
channel.start_consuming()
