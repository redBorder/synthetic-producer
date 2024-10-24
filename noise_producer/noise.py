#!/usr/bin/env python3

from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
import os
import string
from datetime import datetime
import argparse

# Configura el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Inicializa Faker para datos sintéticos
fake = Faker()

# Funciones para generar datos
def generate_msg_names():
    msg_names = [
        'ET SCAN Nmap TCP Connect Scan Detected',
        'ET SCAN Potential SYN Scan Detected',
        'ET SCAN TCP NULL Scan Detected',
        'ET SCAN TCP FIN Scan Detected',
        'ET SCAN TCP Xmas Scan Detected',
        'ET SCAN Potential UDP Scan Detected',
        'ET SCAN Port Sweep Detected',
        'ET SCAN ICMP Sweep Detected',
        'ET SCAN Unusual Port Scanning Detected',
        'ET SCAN Behavioral Unusual Port 80 Traffic Detected',
        'ET SCAN Possible HTTP GET Flood Detected',
        'ET SCAN Potential SSH Scan Detected',
        'ET SCAN Potential SMB Scan Detected',
        'ET SCAN Behavioral Anomalous Port Scanning Detected',
        'ET SCAN High Number of Connection Attempts Detected',
        'ET SCAN Potential FTP Bounce Scan Detected',
        'ET SCAN Unusual Network Reconnaissance Detected',
        'ET SCAN Possible DNS Zone Transfer Attempt',
        'ET SCAN Suspicious Port Scanning Activity Detected',
        'ET SCAN Unusual Outbound Port Scan Detected',
        'ET SCAN Behavior Consistent with Port Scanning Detected',
    ]
    return random.choice(msg_names)

def generate_app_name():
    app_names = [
        "brave-browser.desktop",
        "chrome.desktop",
        "firefox.desktop",
        "mysql.service",
        "apache2.service",
        "nginx.service",
        "ssh.service",
        "vsftpd.service",
        "systemd.service",
        "docker.service"
    ]
    return random.choice(app_names)

# Cargar datos de archivos JSON
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Función para generar direcciones IP realistas
def generate_ip():
    return fake.ipv4_private()  # Genera IPs privadas (puedes cambiar a ipv4_public si necesitas IPs públicas)

def generate_mac():
    return fake.mac_address()

def generate_port():
    return random.randint(1024, 65535)

def generate_hostname():
    prefix = random.choice(['host', 'server', 'node', 'machine', 'localhost'])
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{prefix}-{suffix}"

# Función para generar errores SSL o de red de ejemplo
def generate_error_message():
    errors = [
        "handshake failed; returned -1, SSL error code 1, net_error -202",
        "connection reset; SSL error code 5, net_error -105",
        "certificate validation failed; SSL error code 3, net_error -201",
        "socket timeout; returned -1, SSL error code 2, net_error -204"
    ]
    return random.choice(errors)

# Función para generar raw_message y message
def generate_raw_message(hostname, app_name, procid):
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")  # Ej: "Oct 23 15:22:15"
    error_message = generate_error_message()

    # raw_message incluye todos los elementos
    raw_message = f"<14>{timestamp} {hostname} {app_name}[{procid}]: [266809:266815:1023/{datetime.now().strftime('%H%M%S')}.078218:ERROR:ssl_client_socket_impl.cc(882)] {error_message}"
    
    # message es el contenido del mensaje de error
    message = f"[266809:266815:1023/{datetime.now().strftime('%H%M%S')}.078218:ERROR:ssl_client_socket_impl.cc(882)] {error_message}"

    return raw_message, message

# Funciones para generar eventos de red desde diferentes archivos JSON
# Función para generar eventos de intrusión
def generate_intrusion(data):
    intrusion_data = random.choice(data['intrusions'])  # Selecciona una intrusión aleatoria
    intrusion_data.update({
        "timestamp": int(time.time()),
        "msg": generate_msg_names(),
        "sig_id": random.choice([2001583, 2001581, 2001569, 2001579]),
        "priority": random.choice(['low', 'medium', 'high']),
        "src": generate_ip(),
        "dst": generate_ip(),
        "src_port": generate_port(),
        "dst_port": generate_port()
    })
    return intrusion_data

# Función para generar eventos de flujo (netflow)
def generate_flow(data):
    flow_data = random.choice(data['flows'])  # Selecciona un flujo aleatorio
    flow_data.update({
        "timestamp": int(time.time()),
        "flow_id": random.randint(1000, 9999),
        "type": random.choice(["netflowv10", "netflowv9"]),
        "direction": random.choice(["downstream", "upstream"]),
        "lan_ip": generate_ip(),
        "wan_ip": generate_ip(),
        "client_mac": generate_mac(),
        "lan_l4_port": generate_port(),
        "wan_l4_port": generate_port(),
        "bytes": random.randint(500, 10000),
        "pkts": random.randint(1, 100)
    })
    return flow_data

# Función para generar eventos de vault
def generate_vault(data):
    vault_data = random.choice(data['vaults'])  # Selecciona un vault aleatorio
    hostname = generate_hostname()
    app_name = generate_app_name()
    procid = random.randint(1000, 9999)

    raw_message, message = generate_raw_message(hostname, app_name, procid)

    vault_data.update({
        "timestamp": int(time.time()),
        "hostname": hostname,
        "fromhost_ip": generate_ip(),
        "app_name": app_name,
        "raw_message": raw_message,
        "syslogseverity_text": random.choice(['notice', 'info', 'critical', 'emergency']),
        "message": message
    })
    return vault_data

# Función para intercalar la generación de eventos y enviar a diferentes topics
def send_interleaved_events(duration):
    data = load_json_data('data.json')  # Cargar el archivo unificado
    event_generators = [
        (generate_intrusion, 'rb_event'),
        (generate_flow, 'rb_flow'),
        (generate_vault, 'rb_vault')
    ]

    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            event_func, topic = random.choice(event_generators)
            event_data = event_func(data)
            if event_data:
                producer.send(topic, value=event_data)
                print(f'Data sent to {topic}: {event_data}')
            time.sleep(random.uniform(duration/10, duration/4))  # Al menos 4 picos de tráfico
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
    args = parser.parse_args()
    # Llama a la función para comenzar a enviar los eventos
    send_interleaved_events(args.duration)
