import pika
import time

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

msg_n = 1
while True:
    body = f"Hello ({msg_n})"
    channel.basic_publish(
        exchange='',
        routing_key='holas',
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensaje persistente
            timestamp=int(time.time())
        )
    )
    print(f"[SENDER] Sent: {body}")
    msg_n += 1
    time.sleep(0.8)
