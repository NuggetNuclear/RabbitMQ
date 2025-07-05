# 🐇 RabbitMQ + Scapy MITM Playground

Repositorio para pruebas de interceptación y modificación de tráfico AMQP con Scapy, NetfilterQueue y Docker.

---

## 📂 Carpetas y Archivos


RabbitMQ/
├── docker-compose.yml
├── sender/
│   ├── Dockerfile
│   └── sender_cli.py      # CLI: auto-spam o modo interactivo
├── receiver/
│   ├── Dockerfile
│   └── receiver.py        # imprime cada msg al instante
├── interceptor_nfqueue.py # modifica en vivo: M-1 y M-2
└── heartbeat_bad.py       # inyecta manualmente heartbeat inválido (M-5)

```

---


---

## 🧪 ¿Qué hace cada cosa?

| Script / Contenedor        | Descripción                                                                                  | Detalles                                       |
| ------------------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `rabbitmq`                | Broker AMQP + panel web                                                                      | Puertos: 5672 (AMQP) y 15672 (dashboard)       |
| `sender`                  | Envía mensajes: <br>• Modo interactivo (`-i`) <br>• Modo auto (`--freq`, `-m`)                | Se conecta al broker RabbitMQ                  |
| `receiver`                | Escucha la cola y muestra cada mensaje                                                        | Sin puertos expuestos                          |
| `interceptor_nfqueue.py`  | Intercepta tráfico en vivo usando iptables + NFQUEUE, modifica Channel ID → 0 y frame-end     | Modificaciones M-1 y M-2                       |
| `heartbeat_bad.py`       | Inyecta manualmente un frame heartbeat inválido para provocar que el broker corte la conexión | Modificación M-5                               |

---

## ⚙️ Instalación rápida

```bash
# 1️⃣ Construir imágenes
docker compose build

# 2️⃣ Levantar broker + receiver
docker compose up -d rabbit receiver

# 3️⃣ Ver logs del receiver
docker compose logs -f receiver

# 4️⃣ Enviar mensajes:
#    A) interactivo
docker compose run --rm sender -i

#    B) auto spam cada 0.3 s
docker compose run --rm sender --freq 0.3 -m "Hola"

GUI: [http://localhost:15672](http://localhost:15672) (gabriel / insaid33)

---

## Limpiar todo (El real botón nuclear)

```bash
# apaga y borra contenedores + volúmenes + imágenes del stack
sudo docker compose down -v --rmi all

# botón nuclear global (borrará TODO Docker)
sudo docker system prune -a --volumes --force
```

## Requisitos

* Docker ≥ 20 & Docker Compose v2.

---

## 🔮 Roadmap

- [ ] Laboratorio de captura (Sniffer PCAP)
- [ ] Intercept y Patch con Scapy
- [ ] Fuzzing de payloads AMQP
- [ ] Modificaciones de campos críticos
- [ ] Análisis y métricas de impacto
- [ ] Grabación video demo
- [ ] Empaquetado del repositorio
- [ ] Subida y entrega final

---

## Disclaimer

Este repo es **full vibe coding** mientras aprendo python, ya despues full codigo propio, nada de IA 👺.
