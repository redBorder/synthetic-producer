#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from assets import lan_devices, random_vendor, random_malicious_ip, random_port

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
    (49987, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure arbitrary file upload to tftpRoot attempt', 'low'),
    (52129, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure directory traversal attempt', 'low'),
    (57581, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
    (57582, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
    (57583, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
    (58169, 1, 'SERVER-WEBAPP Microsoft Windows Open Management Infrastructure remote code execution attempt', 'high'),
    (59750, 3, 'SERVER-WEBAPP Cisco Enterprise NFV Infrastructure command injection attempt', 'medium'),
    (59751, 3, 'SERVER-WEBAPP Cisco Enterprise NFV Infrastructure command injection attempt', 'medium'),
    (2033690, 1, 'ET TROJAN Cobalt Strike Infrastructure CnC Domain in DNS Lookup', 'high'),
    (2033691, 1, 'ET TROJAN Cobalt Strike Infrastructure CnC Domain in DNS Lookup', 'high')
]

# Función para generar direcciones IP realistas
def generate_ip():
    return fake.ipv4_private()  # Genera IPs privadas (puedes cambiar a ipv4_public si necesitas IPs públicas)

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
    sig_id_data = random.choice(sig_ids)
    lan_asset = lan_devices[5] # web server
    http_port = random.choice([80, 443])
    return {
        "timestamp": int(time.time()),
        "src_port": random_port(),
        "src_port_name": str(random_port()),
        "dst_port": http_port,
        "dst_port_name": str(http_port),
        "src_asnum": 4110056778,
        "src": random_malicious_ip(),
        "src_name": random_malicious_ip(),
        "dst_asnum": "3038642698",
        "dst_name": lan_asset[0],
        "dst": lan_asset[0],
        "ethsrc": fake.mac_address(),
        "ethdst": lan_asset[1],
        "ethsrc_vendor": random,
        "ethdst_vendor": lan_asset[2],
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "sig_id": sig_id_data[0],  # ID del evento
        "rev": sig_id_data[1],  # Revisión asociada al evento
        "priority": sig_id_data[3],
        "classification": "Command and Control",
        "msg": sig_id_data[2],  # Descripción del mensaje
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "ttl": 47,
        "tos": 0,
        "id": 0,
        "iplen": 92,
        "iplen_range": "[64-128)",
        "dgmlen": 92,
        "group_uuid": "f1b4eeb4-12e1-464c-821f-2439564ec585",
        "group_name": "outside",
        "sensor_type": "ips",
        "domain_name": "N/A",
        "sensor_ip": "10.0.250.195",
        "index_partitions": 5,
        "index_replicas": 1,
        "sensor_uuid": "df699ecd-fc05-41fd-a0a3-87ecd7da2245",
        "sensor_name": "rbips-62ac2c7d",
        "namespace": "Namespace Level Alfa",
        "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
        "organization": "TechSecure",
        "organization_uuid": "4b839195-3d3a-4983-abc0-9731ea731cab",
        "service_provider": "TechSecure Corp",
        "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a",
        "campus": "N/A",
        "campus_uuid": "N/A",
        "building": "Main building",
        "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6"
    }

# Funciones para simular las técnicas de ataque
def acquire_infrastructure():
    print("Adquiriendo infraestructura (T1583): Dominio y servidores C2 adquiridos.")

def develop_capabilities():
    print("Desarrollando capacidades (T1587): Herramientas maliciosas desarrolladas.")

def compromise_accounts():
    print("Comprometiendo cuentas (T1586): Correos de spear-phishing personalizados enviados.")

def resource_development():
    print("Desarrollando recursos (T1583): Recursos necesarios adquiridos para realizar el ataque.")

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            data = generate_event()
            producer.send('rb_event', value=data)  # Envía los eventos al topic de Kafka
            print(f'Data sent: {data}')
            time.sleep(0.1)  # Intervalo entre eventos
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
    args = parser.parse_args()
    run_producer(args.duration)
