import pika
import time
import sys; sys.stdout.reconfigure(line_buffering=True)

parameters = pika.ConnectionParameters(
    'rabbitmq', 5672, '/', pika.PlainCredentials('gabriel', 'insaid33')
)

# –– 20 intentos de conexión, 3 s c/u  ––
for i in range(20):
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[WAIT] RabbitMQ is not ready, retry {i+1}/20…")
        time.sleep(3)
else:
    raise Exception("Couldn't connect to RabbitMQ after 20 attempts. Exiting.")

print("[RECEIVER] Connected to RabbitMQ")
print("[RECEIVER] Ready to receive messages...")
print("[RECEIVER] Waiting for messages (Ctrl+C to exit)...")

channel = connection.channel()
channel.queue_declare(queue='TheQueue', durable=False)

def callback(ch, method, properties, body):
    print(f"[RECEIVER] Got: {body.decode()}")
    print(f"  Delivery tag: {method.delivery_tag}")
    print(f"  Exchange: {method.exchange}")
    print(f"  Routing key: {method.routing_key}")
    print(f"  Properties: {properties}")
    print("")

channel.basic_consume(queue='TheQueue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
