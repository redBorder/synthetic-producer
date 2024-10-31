import random
from device import Device

MALICIOUS_IPS = ["74.125.250.244", "74.125.250.245", "74.125.250.246", "74.125.250.247", "74.125.250.248", "90.167.13.113", "35.230.139.19", "92.249.48.244"]
wan_devices = [
    Device(ip="142.250.190.78", vendor="Google LLC"),  # Google
    Device(ip="157.240.241.35", vendor="Facebook, Inc."),  # Facebook
    Device(ip="104.244.42.193", vendor="Twitter, Inc."),  # Twitter
    Device(ip="151.101.65.140", vendor="Reddit, Inc."),  # Reddit
    Device(ip="13.107.42.14", vendor="Microsoft Corporation"),  # Microsoft
    Device(ip="23.235.47.193", vendor="Cloudflare, Inc."),  # Cloudflare
    Device(ip="185.199.108.153", vendor="GitHub, Inc."),  # Github
    Device(ip="199.232.69.194", vendor="Stack Exchange, Inc."),  # Stack Overflow
    Device(ip="172.217.3.110", vendor="Google LLC"),  # Gmail
    Device(ip="3.213.181.215", vendor="Amazon.com, Inc."),  # Amazon
    Device(ip="104.16.51.111", vendor="Cloudflare, Inc."),  # Cloudflare
    Device(ip="151.101.1.69", vendor="Reddit, Inc."),  # Reddit
    Device(ip="185.199.109.153", vendor="GitHub, Inc."),  # Github
    Device(ip="104.244.42.129", vendor="Twitter, Inc."),  # Twitter
    Device(ip="157.240.3.35", vendor="Facebook, Inc.")  # Instagram
]
wan_devices += [Device(ip=mal) for mal in MALICIOUS_IPS]
lan_devices_2 = [
    Device(ip="192.168.0.1", mac="00:1a:2b:3c:4d:5e", vendor="Cisco Systems, Inc", name="Main Router"),
    Device(ip="192.168.0.10", mac="00:2b:3c:4d:5e:6f", vendor="Cisco Systems, Inc", name="Base Router"),
    Device(ip="192.168.0.20", mac="00:3c:4d:5e:6f:7a", vendor="Cisco Systems, Inc", name="Labs Router"),
    Device(ip="192.168.0.30", mac="00:4d:5e:6f:7a:8b", vendor="TP-Link Corp.", name="Recreational Router"),
    Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
    Device(ip="192.168.0.110", mac="00:6f:7a:8b:9c:0d", vendor="ASUSTek COMPUTER INC.", name="Storeage Server"),
    Device(ip="192.168.3.10", mac="00:8b:9c:0d:1e:2f", vendor="ASUSTek COMPUTER INC.", name="PC Alicia"),
    Device(ip="192.168.3.11", mac="00:9c:0d:1e:2f:3a", vendor="ASUSTek COMPUTER INC.", name="PC Bob"),
    Device(ip="192.168.3.12", mac="00:0d:1e:2f:3a:4b", vendor="ASUSTek COMPUTER INC.", name="PC Carlos"),
    Device(ip="192.168.3.13", mac="00:1e:3a:4b:ff:1a", vendor="Dell Inc.", name="Base Printer")
]

lan_devices = [ #On deprecation
    ("192.168.0.1", "00:1a:2b:3c:4d:5e", "Cisco Systems, Inc"),       #Main Router
    ("192.168.0.10", "00:2b:3c:4d:5e:6f", "Cisco Systems, Inc"),      #BaseRouter
    ("192.168.0.20", "00:3c:4d:5e:6f:7a", "Cisco Systems, Inc"),      #LabsRouter
    ("192.168.0.30", "00:4d:5e:6f:7a:8b", "TP-Link Corp."),           #RecreationalRouter
    ("192.168.0.100", "00:5e:6f:7a:8b:9c", "ASUSTek COMPUTER INC."),  #WebServer
    ("192.168.0.110", "00:6f:7a:8b:9c:0d", "ASUSTek COMPUTER INC."),  #StoreageServer
    ("192.168.3.10", "00:8b:9c:0d:1e:2f", "ASUSTek COMPUTER INC."),   #PCAlicia
    ("192.168.3.11", "00:9c:0d:1e:2f:3a", "ASUSTek COMPUTER INC."),   #PCBob
    ("192.168.3.12", "00:0d:1e:2f:3a:4b", "ASUSTek COMPUTER INC."),   #PCCarlos
    ("192.168.3.13", "00:1e:3a:4b:ff:1a", "Dell Inc.")                #BasePrinter
]

user_devices_2 = [
    Device(ip="192.168.3.10", mac="00:1a:2b:3c:4d:5e", vendor="ASUSTek COMPUTER INC.", name="PCAlice"),
    Device(ip="192.168.3.11", mac="00:2b:3c:4d:5e:6f", vendor="ASUSTek COMPUTER INC.", name="PCBob"),
    Device(ip="192.168.3.12", mac="00:3c:4d:5e:6f:7a", vendor="ASUSTek COMPUTER INC.", name="PCCarlos"),
    Device(ip="192.168.3.13", mac="00:4d:5e:6f:7a:8b", vendor="Dell Inc.", name="BasePrinter")
]

mirror_devices = [
#    Device(ip="192.168.0.1", mac="00:1a:2b:3c:4d:5e", vendor="Cisco Systems, Inc", name="MainRouter"),
   Device(ip="192.168.0.10", mac="00:2b:3c:4d:5e:6f", vendor="Cisco Systems, Inc", name="BaseRouter"),
   Device(ip="192.168.0.20", mac="00:3c:4d:5e:6f:7a", vendor="Cisco Systems, Inc", name="LabsRouter"),
   Device(ip="192.168.0.30", mac="00:4d:5e:6f:7a:8b", vendor="TP-Link Corp.", name="RecreationalRouter")
]

web_devices = [
   Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="WebServer"),
   Device(ip="192.168.0.110", mac="00:6f:7a:8b:9c:0d", vendor="ASUSTek COMPUTER INC.", name="StoreageServer")
]

network_devices = mirror_devices + web_devices
lan_devices_2 = user_devices_2 + network_devices

user_devices = [
    ("192.168.3.10", "00:1a:2b:3c:4d:5e", "ASUSTek COMPUTER INC.", "PCAlice"),
    ("192.168.3.11", "00:2b:3c:4d:5e:6f", "ASUSTek COMPUTER INC.", "PCBob"),
    ("192.168.3.12", "00:3c:4d:5e:6f:7a", "ASUSTek COMPUTER INC.", "PCCarlos"),
    ("192.168.3.13", "00:4d:5e:6f:7a:8b", "Dell Inc.", "BasePrinter")]

def random_lan():
  return random.choice(lan_devices)

def random_mac():
    return f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"

def random_port():
  random.choice(list(range(10000,60000)))

def random_malicious_ip():
  random.choice(MALICIOUS_IPS)

def random_wan():
  return random.choice(wan_devices)
def random_vendor():
   return random.choice([
       "Cisco Systems, Inc",
       "Dell Inc.",
       "HP Inc.",
       "ASUSTek COMPUTER INC.",
       "TP-Link Corp.",
       "Netgear Inc.",
       "D-Link Corp.",
       "Intel Corporation",
       "Apple Inc.",
       "Lenovo Group Ltd.",
       "Samsung Electronics Co.",
       "Microsoft Corporation",
       "Huawei Technologies Co.",
       "Sony Corporation",
       "LG Electronics Inc.",
       "Acer Inc."
   ])
   