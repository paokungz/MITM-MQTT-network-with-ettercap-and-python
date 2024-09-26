# MITM MQTT with Ettercap and Paho-MQTT

This project demonstrates a Man-in-the-Middle (MITM) attack on MQTT (Message Queuing Telemetry Transport) using Ettercap and Paho-MQTT. The repository includes scripts to intercept and modify MQTT messages and an example of ARP spoofing using Ettercap.

## Features

- **ARP Spoofing with Ettercap**: Perform a MITM attack using Ettercap to intercept MQTT packets.
- **MQTT Message Interception**: Python scripts using Paho-MQTT to subscribe to topics, modify messages, and republish them.
- **Customizable**: The Python script can be adapted to target specific MQTT messages and brokers.

## Getting Started

### Prerequisites

- **Python 3.x**: Required for running the Paho-MQTT scripts.
- **Ettercap**: Network security tool for MITM attacks.
- **Paho-MQTT**: Python MQTT client library for interacting with the MQTT broker.

### Installation

1. **Install Paho-MQTT**: 
   ```bash
   pip install paho-mqtt
2. **install Ettercap
   ```bash
   sudo apt-get install ettercap-text-only
### Step 2: Perform ARP Spoofing with Ettercap
   ```bash
   sudo ettercap -T -q -i <your interface> -M arp:remote /<ip1>// /<ip2>//
### Step 3: Run the MQTT Interceptor Script
