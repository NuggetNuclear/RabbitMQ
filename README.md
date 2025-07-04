## 📂 Carpetas y Archivos

```
RabbitMQ/
├── docker-compose.yml
├── sender/
│   ├── Dockerfile
│   └── sender_cli.py          # CLI: auto‑spam o modo interactivo
├── receiver/
│   ├── Dockerfile
│   └── receiver.py            # imprime cada msg al instante
```

---

## ¿Qué hace cada cosa?

| Contenedor   | Rol dramático                                                                           | Puertos / Flags           |
| ------------ | --------------------------------------------------------------------------------------- | ------------------------- |
| **rabbitmq** | Broker AMQP + UI web                                                                    | 5672 (AMQP) · 15672 (GUI) |
| **receiver** | Se suscribe a la cola `TheQueue` y chilla cada mensaje con `flush=True`                    | ningún puerto expuesto    |
| **sender**   | Envia mensajes: <br>- **Modo auto** (`--freq` & `-m`) <br>- **Modo interactivo** (`-i`) | STDIN/TTY habilitado      |

El compose los conecta en una red `rabbitmq-net` (192.168.20.0/24) para que se vean por hostname.

---

## Instalación express

```bash
# 1️⃣ Construye imágenes
docker compose build

# 2️⃣ Arranca broker + receptor en background
docker compose up -d rabbit receiver

# 3️⃣ En otra terminal para ver los logs del receiver
docker compose logs -f receiver

# 4️⃣ Mandar mensajes
#    A) interactivo
docker compose run --rm sender -i
#    B) turbo loop cada 0.3 s
docker compose run --rm sender --freq 0.3 -m "Hola"
```

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
