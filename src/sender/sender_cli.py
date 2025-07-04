# sender_cli.py
import pika, sys, time, argparse


parser = argparse.ArgumentParser(
    description="RabbitMQ message sender",
)
parser.add_argument("--freq", "-f", type=float, default=1.0,
                    help="Seconds between messages (default 1.0)")
parser.add_argument("--msg", "-m", default="Hello",
                    help="Base message text (default 'Hello')")
parser.add_argument("--interactive", "-i", action="store_true",
                    help="Interactive mode: read lines from stdin")
args = parser.parse_args()

# –– 20 intentos de conexión, 3 s c/u  ––
params = pika.ConnectionParameters(
    "rabbitmq", 5672, "/", pika.PlainCredentials("gabriel", "insaid33")
)
for i in range(20):
    try:
        conn = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[WAIT] RabbitMQ is not ready, retry {i+1}/20…", flush=True)
        
        time.sleep(3)
else:
    sys.exit("Couldn't connect to RabbitMQ after 20 attempts. Exiting.")

ch = conn.channel()
ch.queue_declare(queue="TheQueue", durable=False)

def send(body):
    ch.basic_publish(
        exchange="",
        routing_key="TheQueue",
        body=body.encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"[SENDER] Sent: {body}", flush=True)

if args.interactive:
    print("Type + Enter to send (Ctrl-D = exit)")
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
