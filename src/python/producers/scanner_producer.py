#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from random import shuffle
# from assets import lan_devices, random_wan, wan_devices
import assets

# Define sig_ids list
# sig_ids = [1, 2, 3, 4, 5]  # Add appropriate signature IDs

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

fake = Faker() # Useful to generate random values depending on the field

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  lan_device = random.choice(assets.lan_devices_2)
  # wan_device = random.choice(wan_devices)
  # in_out = [lan_device, wan_device]
  # shuffle(in_out)
  # src_device = in_out[0]
  # dst_device = in_out[1]
  # sensor = random.choice(assets.mirror_devices)
  # direction = 'upstream' if src_device == lan_device else 'downstream'
  # domain = '.'.join(wan_device.url.split('.')[-2:])
  # www = 'www.' + domain
  timestamp = int(time.time())
  # date = time.localtime(timestamp)
  # # Weights based on day of week (0=Monday, 6=Sunday)
  # day_weights = {
  #     0: 1.0,  # Monday
  #     1: 0.8,  # Tuesday
  #     2: 1.0,  # Wednesday
  #     3: 0.7,  # Thursday
  #     4: 0.5,  # Friday
  #     5: 0.1,  # Saturday
  #     6: 0.1   # Sunday
  # }
  # # Weights based on hour (0-23)
  # hour_weights = {
  #     0: 1.0, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
  #     6: 0.1, 7: 0.5, 8: 0.6, 9: 1.0, 10: 1.0, 11: 1.0,
  #     12: 0.8, 13: 0.5, 14: 1.0, 15: 0.9, 16: 0.5, 17: 0.3,
  #     18: 0.1, 19: 0.1, 20: 0.1, 21: 0.1, 22: 0.1, 23: 0.1
  # }
  # weight = day_weights[date.tm_wday] * hour_weights[date.tm_hour]    
  # pkt = random.randint(10,1000) *weight
  # bytes = pkt*100
  return {
    "timestamp": timestamp,
    # device prop
    "ipv4": lan_device.ip,
    "os": lan_device.os,
    # vuln prop
    "product": "OpenSSH",
    "cpe": "cpe:2.3:a:openbsd:openssh:5.3",
    "version": "5.3",
    "protocol": "tcp",
    "port_state": "open",
    "port": "22",
    # sensor prop
    "name": "Scanner",
    "uuid": "a44e727f-a1ec-499b-b26d-982445c302db", # TODO: put uuid of scanner sensor
    "scan_id": "1",                                 # TODO: put uuid of scanner sensor
    "scan_type": "2"
    # "servicename": 'null'
  }

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
  start_time = time.time()
  try:
    while duration < 0 or time.time() - start_time < duration:
      data = generate_event()
      producer.send('rb_scanner', value=data)  # Envía los eventos al topic de Kafka
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
