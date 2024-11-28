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

fake = Faker()

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
    domain = '.'.join(wan_device.url.split('.')[-2:])
    www = 'www.' + domain
    timestamp = int(time.time())
    date = time.localtime(timestamp)
    # Weights based on day of week (0=Monday, 6=Sunday)
    day_weights = {
        0: 1.0,  # Monday
        1: 0.8,  # Tuesday
        2: 1.0,  # Wednesday
        3: 0.7,  # Thursday
        4: 0.5,  # Friday
        5: 0.1,  # Saturday
        6: 0.1   # Sunday
    }
    # Weights based on hour (0-23)
    hour_weights = {
        0: 1.0, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
        6: 0.1, 7: 0.5, 8: 0.6, 9: 1.0, 10: 1.0, 11: 1.0,
        12: 0.8, 13: 0.5, 14: 1.0, 15: 0.9, 16: 0.5, 17: 0.3,
        18: 0.1, 19: 0.1, 20: 0.1, 21: 0.1, 22: 0.1, 23: 0.1
    }
    weight = day_weights[date.tm_wday] * hour_weights[date.tm_hour]    
    pkt = random.randint(10,1000) *weight
    bytes = pkt*100
    return {
        "http_url": www, #"https://www.example.com/path/to/resource?param=value",
        "referer": www, #"https://www.example.com/path/to/resource?param=value",
        "http_host": www, #"www.example.com",
        "host": www, #"www.example.com",
        "http_host_l2": domain, #"example.com",
        "host_l2_domain": domain, #"example.com",
        "referer_l2": domain, #"example.com",
        "http_user_agent": fake.user_agent(),
        "type": "netflowv10",
        "ip_protocol_version": 4,
        "l4_proto": 17, 
        "l4_proto_name": "udp",
        "input_vrf": 0, 
        "flow_end_reason": "idle timeout",
        # "biflow_direction": "initiator",
        "application_id_name": assets.random_application(), 
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
        "sensor_uuid": sensor.uuid,
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
        "timestamp": timestamp
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