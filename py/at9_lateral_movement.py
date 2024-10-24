#!/usr/bin/env python3
from kafka import KafkaProducer
import json
import time
import random
from assets import lan_devices, random_port

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Función para generar eventos de escaneo activo (Active Scanning T1595)
def generate_event():
    src_port = random_port()
    dst_port = random_port()
    return {
        "src": "192.168.3.12",
        "dst": "192.168.3.10",
        "ethsrc": lan_devices['192.168.3.12'],
        "ethdst": lan_devices['192.168.3.10'],
        "payload": "73726567417265736f75746f722e436f726574726f737465722e437573746f6d65722e4e65775f4974656d205c4d696170706c69636174696f6e2e70776f772e4b6f706572696e672e417267757365727261636f69737469732e484b43552e5c4d696170706c69636174696f6e5c4d694170706c69636174696f6e205665727375732e486f6c614d756e646f726272696172732e486b43552e4e65775f4974656d205354505265673274636f726574726f737465722e4e65775f4974656d20566973696f6e202053656e64696e672e4d726f6f7420546f6b656e68616d616e204874617420436c61757365",
        "timestamp": int(time.time()),
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "rev": 3,
        "priority": "high",
        "classification": "Trojan",
        "msg": 'POLICY-OTHER use of psexec remote administration tool',
        "sig_id": 24008,  # Selecciona un sig_id aleatorio
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethsrc_vendor": "ASUSTek COMPUTER INC.",
        "ethdst_vendor": "ASUSTek COMPUTER INC.",
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "src_port": src_port,
        "src_port_name": str(src_port),
        "dst_port": dst_port,
        "dst_port_name": str(dst_port),
        "src_asnum": 4110056778,
        "dst_asnum": "3038642698",
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

# Produce mensajes continuamente simulando eventos de escaneo activo
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
