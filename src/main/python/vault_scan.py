#!/usr/bin/env python3
"""
Synthetic Data Producer for Security Scan Events

This script generates synthetic security scan events and publishes them to the Kafka topic rb_vault.
It simulates various types of network scanning activities and security alerts that might
be detected in a redborder environment.

The script uses:
- Kafka Producer: To send messages to a Kafka broker
- Faker: To generate realistic synthetic data
- Random: For randomizing event selection and data generation

Dependencies:
    - kafka-python
    - faker
    - python 3.x

Environment Setup:
    - Requires a running Kafka broker on localhost:9092
    - Requires proper network connectivity to Kafka

Usage:
    Run directly with Python 3:
    $ python3 vault_scan.py
"""

from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
import os
import string
from datetime import datetime

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
        # "fromhost_ip": random.choice(['192.168.0.12', '192.168.3.11', '192.168.4.50']),
        "fromhost_ip": generate_ip(),
        "app_name": app_name,
        "raw_message": raw_message,
        "syslogseverity_text": random.choice(['notice', 'info', 'critical', 'emergency']),
        "message": message
    })
    return vault_data

# Función para intercalar la generación de eventos y enviar a diferentes topics
def send_interleaved_events():
    data = load_json_data('/etc/synthetic-producer/python/vault.json')  # Cargar el archivo unificado
    event_generators = [
        (generate_vault, 'rb_vault')
    ]

    try:
        while True:
            event_func, topic = random.choice(event_generators)
            event_data = event_func(data)
            if event_data:
                producer.send(topic, value=event_data)
                print(f'Data sent to {topic}: {event_data}')
            time.sleep(random.uniform(0.5, 2.5))  # Simular picos de tráfico
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()

# Llama a la función para comenzar a enviar los eventos
send_interleaved_events()
