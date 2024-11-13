#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from random import shuffle
from assets import lan_devices, random_wan, wan_devices
import assets

# Define sig_ids list
sig_ids = [1, 2, 3, 4, 5]  # Add appropriate signature IDs

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


# Función para generar eventos sintéticos relacionados con redes
def generate_event():
    lan_device = random.choice(assets.lan_devices_2)
    wan_device = random.choice(wan_devices)
    in_out = [lan_device, wan_device]
    shuffle(in_out)
    src_device = in_out[0]
    dst_device = in_out[1]
    sensor = random.choice(assets.mirror_devices)
    direction = 'upstream' if src_device == lan_device else 'downstream'
    pkt = random.randint(10,1000)
    bytes = pkt*100
    return {
        "type": "netflowv9",
        "ip_protocol_version": 4,
        "l4_proto": 17, 
        "l4_proto_name": "udp",
        "input_vrf": 0, 
        "flow_end_reason": "idle timeout",
        # "biflow_direction": "initiator",
        # "application_id_name": "13:443", 
        "engine_id_name": "13",
        "output_vrf": 0, 
        "lan_interface": 1, 
        "lan_interface_name": "1", 
        "lan_interface_description": "LAN Interface",
        "wan_interface": 14, "wan_interface_name": "14",
        "wan_interface_description": "WAN Interface",
        "client_mac_vendor": "Cisco Systems",
        "index_partitions": 5, 
        "index_replicas": 1, 
        "sensor_ip": sensor.ip, 
        "sensor_name": sensor.name, 
        "namespace": "Namespace Level Alfa", 
        "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
        "organization": "TechSecure", 
        "organization_uuid": "4b839195-3d3a-4983-abc0-9731ea731cab",
        "service_provider": "TechSecure Corp", 
        "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a", 
        "building": "Main building",
        "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6",
        "direction": direction, 
        "lan_ip": lan_device.ip, 
        "wan_ip": wan_device.ip,
        "public_ip": wan_device.ip, 
        "client_mac": sensor.mac,
        "lan_l4_port": assets.random_port(),
        "wan_l4_port": assets.random_port(),
        "bytes": bytes,
        "pkts": pkt,        
        "timestamp": int(time.time())
    }

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            data = generate_event()
            producer.send('rb_flow', value=data)  # Envía los eventos al topic de Kafka
            print(f'Data sent: {data}')
            time.sleep(random.uniform(0.000001, 0.01))  # Random interval between events    except KeyboardInterrupt:
        pass
    finally:
        producer.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5), -1 for infinite')
    args = parser.parse_args()
    run_producer(args.duration)