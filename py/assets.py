import random
lan_devices = [
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

def random_lan():
  return random.choice(lan_devices)

def random_mac():
    return f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}"

def random_port():
  random.choice(list(range(10000,60000)))

def random_malicious_ip():
  random.choice(["74.125.250.244", "74.125.250.245", "74.125.250.246", "74.125.250.247", "74.125.250.248", "90.167.13.113", "35.230.139.19", "92.249.48.244"])