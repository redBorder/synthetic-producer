import random
from device import Device

MALICIOUS_IPS = ["74.125.250.244", "74.125.250.245", "74.125.250.246", "74.125.250.247", "74.125.250.248", "90.167.13.113", "35.230.139.19", "92.249.48.244"]
wan_devices = [
    Device(ip="142.250.190.78", vendor="Google LLC",            url="google.com"),  
    Device(ip="157.240.241.35", vendor="Facebook, Inc.",        url="facebook.com"), 
    Device(ip="104.244.42.193", vendor="Twitter, Inc.",         url="twitter.com"), 
    Device(ip="151.101.65.140", vendor="Reddit, Inc.",          url="reddit.com"),  
    Device(ip="13.107.42.14", vendor="Microsoft Corporation",   url="microsoft.com"),  
    Device(ip="23.235.47.193", vendor="Cloudflare, Inc.",       url="cloudflare.com"),  
    Device(ip="185.199.108.153", vendor="GitHub, Inc.",         url="github.com"),  
    Device(ip="199.232.69.194", vendor="Stack Exchange, Inc.",  url="stackoverflow.com"), 
    Device(ip="172.217.3.110", vendor="Google LLC",             url="gmail.com"), 
    Device(ip="3.213.181.215", vendor="Amazon.com, Inc.",       url="amazon.com"), 
    Device(ip="104.16.51.111", vendor="Cloudflare, Inc.",       url="cloudflare.com"),  
    Device(ip="151.101.1.69", vendor="Reddit, Inc.",            url="reddit.com"), 
    Device(ip="185.199.109.153", vendor="GitHub, Inc.",         url="github.com"),  
    Device(ip="104.244.42.129", vendor="Twitter, Inc.",         url="twitter.com"), 
    Device(ip="157.240.3.35", vendor="Facebook, Inc.",          url="instagram.com")
]
wan_devices += [Device(ip=mal) for mal in MALICIOUS_IPS]
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
    Device(ip="192.168.3.10", mac="00:1a:2b:3c:4d:5e", vendor="ASUSTek COMPUTER INC.", name="PC Alice"),
    Device(ip="192.168.3.11", mac="00:2b:3c:4d:5e:6f", vendor="ASUSTek COMPUTER INC.", name="PC Bob"),
    Device(ip="192.168.3.12", mac="00:3c:4d:5e:6f:7a", vendor="ASUSTek COMPUTER INC.", name="PC Carlos"),
    Device(ip="192.168.3.13", mac="00:4d:5e:6f:7a:8b", vendor="Dell Inc.", name="Base Printer")
]

mirror_devices = [
#    Device(ip="192.168.0.1", mac="00:1a:2b:3c:4d:5e", vendor="Cisco Systems, Inc", name="Main Router"),
   Device(ip="192.168.0.10", mac="00:2b:3c:4d:5e:6f", vendor="Cisco Systems, Inc", name="Base Router", uuid='08eac42f-bf2d-4996-865f-9f6a4f493f71', os="Cisco Unified Communications Manager VoIP adapter"),
   Device(ip="192.168.0.20", mac="00:3c:4d:5e:6f:7a", vendor="Cisco Systems, Inc", name="Labs Router", uuid='0366221c-ecf6-48d2-a5a2-8529346eab54', os="Cisco Unified Communications Manager VoIP adapter"),
   Device(ip="192.168.0.30", mac="00:4d:5e:6f:7a:8b", vendor="TP-Link Corp.", name="Recreational Router", uuid='3e14fd96-1086-4b0a-b3ce-87b0c6863c50', os="TP-Link Router Firmware")]

web_devices = [
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.100", mac="00:5e:6f:7a:8b:9c", vendor="ASUSTek COMPUTER INC.", name="Web Server"),
  Device(ip="192.168.0.110", mac="00:6f:7a:8b:9c:0d", vendor="ASUSTek COMPUTER INC.", name="Storeage Server")
]

network_devices = mirror_devices + web_devices
lan_devices_2 = user_devices_2 + network_devices

user_devices = [
    ("192.168.3.10", "00:1a:2b:3c:4d:5e", "ASUSTek COMPUTER INC.", "PC Alice"),
    ("192.168.3.11", "00:2b:3c:4d:5e:6f", "ASUSTek COMPUTER INC.", "PC Bob"),
    ("192.168.3.12", "00:3c:4d:5e:6f:7a", "ASUSTek COMPUTER INC.", "PC Carlos"),
    ("192.168.3.13", "00:4d:5e:6f:7a:8b", "Dell Inc.", "Base Printer")]

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

def random_application():
  return random.choice([
    "13:443","13:443","13:443","13:443",
    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",    "HTTP",
    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",    "HTTPS",
    "FTP",
    "SSH",
    "SMTP",
    "POP3",
    "IMAP",
    "DNS",    "DNS",
    "DNS",
    "DNS",
    "DNS",
    "DNS",
    "DNS",
    "DHCP",
    "NTP",
    "Telnet",
    "SNMP",    "SNMP",
    "SNMP",
    "SNMP",
    "SNMP",
    "SNMP",
    "LDAP",    "LDAP",    "LDAP",    "LDAP",    "LDAP",    "LDAP",    "LDAP",    "LDAP",
    "RDP",
    "VNC",
    "RTSP",
    "RTP",
    "RTCP",
    "SIP",    "SIP",    "SIP",    "SIP",    "SIP",    "SIP",    "SIP",
    "STUN",
    "TURN",
    "ICE",
    "DTLS",
    "CoAP",
    "MQTT",
    "XMPP",
    "XMPP-TLS",
    "XMPP-STARTTLS",
    "XMPP-SASL",
    "XMPP-SASL-PLAIN",
    "XMPP-SASL-DIGEST-MD5",
    "XMPP-SASL-DIGEST-MD5-CHALLENGE",
    "XMPP-SASL-DIGEST-MD5-CHALLENGE-RESPONSE"
  ])