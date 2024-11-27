#!/usr/bin/env python3
from kafka import KafkaProducer
import json
import time
import random
import assets

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Función para generar eventos sintéticos relacionados con redes

NS= "352369f8-60fb-4b72-a603-d1d8393cca0a"
def generate_event(monitor):
    sensor = random.choice(assets.mirror_devices)
    return {
        'sensor_name': sensor.name,
        'sensor_uuid': sensor.uuid,
        'service_provider': 'TechSecure Corp',
        "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a",
        'organization': 'TechSecure',
        'organization_uuid': '4b839195-3d3a-4983-abc0-9731ea731cab',
        "namespace": "Namespace Level Alfa",
        "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
        'building': 'Main building',
        "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6",
        "index_partitions":5,
        "index_replicas":1,
        'monitor': monitor.monitor,
        'value': monitor.value,
        'type': monitor.type,
        'unit': monitor.unit,
        "timestamp": int(time.time())
    }

class MonitorEvent:
    MONITOR_CONFIGS = {
        'cpu': {            'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
        'memory': {         'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
        'memory_buffer': {  'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
        'memory_cache': {   'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
        'swap': {           'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
        'disk_load': {      'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
        'pch_temp': {       'unit': 'celsius', 'value_range': (25, 50), 'type': 'system', 'is_int': True},
        'system_temp': {    'unit': 'celsius', 'value_range': (25, 50), 'type': 'system', 'is_int': True},
        'avio': {           'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
        'disk': {           'unit': '%', 'value_range': (1.0, 10.0), 'type': 'snmp'},
        'fan': {            'unit': 'rpm', 'value_range': (1000, 5000), 'type': 'system'}
    }    
    def __init__(self, type: str):
        # if type not in ['cpu', 'memory', 'disk', 'network', 'system_temp', 'avio', 'fan', 'load_1', 'disk_load']:
        #     raise ValueError("Invalid monitor type. Must be one of: cpu, memory, disk, network, system_temp, avio, fan, load_1, disk_load")
        self.monitor = type
        self.define_by_type()
    
    @classmethod
    def generate_all_monitors(cls):
        """
        cls es una referencia a la clase misma (MonitorEvent en este caso).
        Permite acceder a atributos y métodos de la clase sin necesidad de crear una instancia.
        Similar a 'self' pero para métodos de clase en lugar de métodos de instancia.
        """        
        monitor_types = cls.MONITOR_CONFIGS.keys()
        return [MonitorEvent(type) for type in monitor_types]        
    def define_by_type(self):
        try:
            config = self.MONITOR_CONFIGS[self.monitor]
        except KeyError:
            raise ValueError(f"Invalid monitor type. Must be one of: {', '.join(self.MONITOR_CONFIGS.keys())}")
        self.unit = config['unit']
        self.type = config['type']
        if config.get('is_int', False):
            self.value = random.randint(*config['value_range'])
        else:
            self.value = '{:.6f}'.format(random.uniform(*config['value_range']))

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            for monitor in MonitorEvent.generate_all_monitors():
                data = generate_event(monitor)
                producer.send('rb_monitor', value=data)  # Envía los eventos al topic de Kafka
                print(f'Data sent: {data}')
            time.sleep(30)
        pass
    finally:
        producer.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5), -1 for infinite')
    args = parser.parse_args()
    run_producer(args.duration)