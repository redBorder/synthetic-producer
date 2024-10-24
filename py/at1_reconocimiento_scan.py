#!/usr/bin/env python3
from kafka import KafkaProducer
import json
import time
import random
from assets import lan_devices, random_malicious_ip, random_port, random_mac

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Active Scanning T1595
def generate_active_scanning_event():
    lan_ip, lan_mac = random.choice(list(lan_devices.items()))   
    port_src = random_port()
    wan_ip = random_malicious_ip()
    return {
        "timestamp": int(time.time()),
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "sig_id": 2001583,
        "rev": 3,
        "priority": "low",
        "classification": "Misc activity",
        "msg": "ET SCAN Behavioral Unusual Port 1433 traffic Potential Scan or Infection",
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethsrc": random_mac(),
        "ethdst": lan_mac,
        "ethsrc_vendor": random.choice(["Cisco Systems, Inc", "Dell Inc.", "HP Inc.", "Intel Corporation", "Apple Inc.", "Samsung Electronics", "Juniper Networks", "IBM Corp.", "Sony Corporation", "LG Electronics", "Huawei Technologies", "ASUS", "Lenovo", "D-Link Corporation", "NetGear", "TP-Link Technologies"]),
        "ethdst_vendor": "ASUSTek COMPUTER INC.", # maybe change between cisco and asus
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "src_port": port_src,
        "src_port_name": str(port_src),
        "dst_port": 1433,
        "dst_port_name": "1433",
        "src_asnum": 4110056778,
        "src": wan_ip,
        "src_name": wan_ip,
        "dst_asnum": "3038642698",
        "dst_name": lan_ip,
        "dst": lan_ip,
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
            data = generate_active_scanning_event()
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
    