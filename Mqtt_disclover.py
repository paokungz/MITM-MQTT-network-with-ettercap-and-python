from scapy.all import *
from struct import unpack

# Filter to capture only MQTT packets (port 1883)
MQTT_PORT = 1883

def mqtt_packet_callback(packet):
    if packet.haslayer(TCP) and packet[TCP].dport == MQTT_PORT:
        mqtt_payload = bytes(packet[TCP].payload)
        if len(mqtt_payload) > 0:
            print("[+] MQTT Packet Captured")
            parse_mqtt_packet(mqtt_payload)
            
def parse_mqtt_packet(payload):
    try:
        # Extract MQTT packet type and topic if possible
        packet_type = payload[0] >> 4
        print(f"[*] MQTT Packet Type: {packet_type}")
        
        if packet_type == 3:  # PUBLISH packet
            print("[*] PUBLISH packet detected")
            
            # Extract remaining length
            remaining_length = payload[1]
            
            # Topic length (bytes 2 and 3)
            topic_length = unpack("!H", payload[2:4])[0]
            
            # Topic (next 'topic_length' bytes)
            topic = payload[4:4+topic_length].decode()
            print(f"[+] Topic: {topic}")
            
            # Message Payload (after the topic)
            message = payload[4+topic_length:].decode()
            print(f"[+] Message: {message}")
            
    except Exception as e:
        print(f"[-] Failed to parse MQTT packet: {e}")

# Start sniffing on the network interface
print("[*] Starting packet sniffing...")
sniff(iface="eth0", filter=f"tcp port {MQTT_PORT}", prn=mqtt_packet_callback, store=0)

