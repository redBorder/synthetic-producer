import random
from faker import Faker

class Device:
    def __init__(self, ip, mac=None, vendor=None, name=None, uuid=None, url=None, os=None):
        self.ip = ip
        fake = Faker()
        self.mac = mac if mac else fake.mac_address()
        self.vendor = vendor if vendor else random.choice(['Cisco Systems, Inc', 'TP-Link Corp.', 'ASUSTek COMPUTER INC.', 'Dell Inc.'])
        self.name = name if name else f"Device_{random.randint(1000,9999)}"
        self.uuid = uuid if uuid else fake.uuid4()
        self.url = url if url else fake.url()
        vendor_os_map = {
            'Dell Inc.': ['Windows'],
            'ASUSTek COMPUTER INC.': ['iOS', 'MacOS'],
            'TP-Link Corp.': ['TP-Link Router Firmware'],
            'Cisco Systems, Inc': ['Cisco Unified Communications Manager VoIP adapter']
        }
        default_os = ['Windows', 'Linux', 'MacOS', 'iOS', 'Android']
        self.os = os if os else random.choice(vendor_os_map.get(self.vendor, default_os))
    def __str__(self):
        if self.name:
            return f"{self.name} ({self.ip}, {self.mac}, {self.vendor}, {self.uuid}, {self.url}, {self.os})"
        return f"({self.ip}, {self.mac}, {self.vendor}, {self.uuid}, {self.url}, {self.os})"

    def __repr__(self):
        if self.name:
            return f"Device(ip='{self.ip}', mac='{self.mac}', vendor='{self.vendor}', name='{self.name}', uuid='{self.uuid}', url='{self.url}', os='{self.os}')"
        return f"Device(ip='{self.ip}', mac='{self.mac}', vendor='{self.vendor}', uuid='{self.uuid}', url='{self.url}', os='{self.os}')"
    @classmethod
    def from_tuple(cls, device_tuple):
        return cls(*device_tuple)    
# class Sensor(Device):
#     def __init__(self, ip, mac=None, vendor=None, name=None, uuid=None):
#         super().__init__(ip, mac, vendor, name)
#         fake = Faker()
#         self.uuid = uuid if uuid else fake.uuid4()

#     def __str__(self):
#         return f"{super().__str__()} [UUID: {self.uuid}]"

#     def __repr__(self):
#         base_repr = super().__repr__()[:-1]  # Remove the closing parenthesis
#         return f"{base_repr}, uuid='{self.uuid}')"

#     @classmethod
#     def from_tuple(cls, sensor_tuple):
#         return cls(*sensor_tuple)
