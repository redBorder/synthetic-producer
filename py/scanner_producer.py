#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from random import shuffle
# from assets import lan_devices, random_wan, wan_devices
import assets
from vulnerability import Vulnerability

# Define sig_ids list
# sig_ids = [1, 2, 3, 4, 5]  # Add appropriate signature IDs

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

fake = Faker() # Useful to generate random values depending on the field

# Función para generar eventos sintéticos relacionados con redes
def generate_event(vulnerability):
  lan_device = random.choice(assets.lan_devices_2)
  timestamp = int(time.time())
  return {
    "timestamp": timestamp,
    # device prop
    "ipv4": lan_device.ip,
    "os": lan_device.os,
    # vuln prop
    "product": vulnerability.product,
    "cpe": vulnerability.cpe,
    "version": vulnerability.version,
    "protocol": vulnerability.protocol,
    "port_state": vulnerability.port_state,
    "port": vulnerability.port,
    # sensor prop
    "name": "Scanner",
    "uuid": "a44e727f-a1ec-499b-b26d-982445c302db", # TODO: put uuid of scanner sensor
    "scan_id": "1",                                 # TODO: put uuid of scanner sensor
    "scan_type": "2"
  }
# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
  start_time = time.time()
  vulnerabilities = Vulnerability.make_vulnerabilities()
  while duration < 0 or time.time() - start_time < duration:
    for v in vulnerabilities:
      data = generate_event(v)
      producer.send('rb_scanner', value=data)  # Envía los eventos al topic de Kafka
      print(f'Data sent: {data}')
      time.sleep(random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]))
  producer.close()

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5), -1 for infinite')
  args = parser.parse_args()
  run_producer(args.duration)
