import re
import paho.mqtt.client as mqtt
import argparse

# This function is triggered when a message is received
def on_message(client, userdata, msg):
    global last_modified_value

    # Convert payload from byte to string
    payload = msg.payload.decode()

    # Use regex to find a numerical value in the message
    match = re.search(r"[-+]?\d*\.\d+|\d+", payload)
    if match:
        try:
            # Convert the extracted value to float
            original_value = float(match.group())

            # Check if this message has already been modified
            if msg.topic in last_modified_value and last_modified_value[msg.topic] == original_value:
                return  # If already modified, do not modify again

            # Modify the value by adding 100
            new_value = original_value + 100
            last_modified_value[msg.topic] = new_value  # Store the modified value to avoid re-sending

            print(f"Received message from topic {msg.topic}: {payload}")
            client.publish(msg.topic, str(new_value))  # Send the modified message back to the topic
            print(f"Sent modified message to topic {msg.topic}: {new_value}")
        
        except ValueError:
            print(f"Payload is not a number: {payload}")  # If the payload is not a number, report it
    else:
        print(f"No numerical value in payload: {payload}")  # If no number is found, report it

# Accept command-line arguments
parser = argparse.ArgumentParser(description="MQTT message interceptor and modifier.")
parser.add_argument('-b', '--broker', required=True, help='Broker IP or address')
parser.add_argument('-t', '--topic', required=True, nargs='+', help='List of topics to subscribe to')

args = parser.parse_args()

broker = args.broker  # Get the broker address from command line
topics = args.topic   # Get the list of topics to subscribe to

# Dictionary to store the last modified value to avoid re-sending
last_modified_value = {}

# Set up the client to use MQTT protocol version 5
client = mqtt.Client(protocol=mqtt.MQTTv5)

# Connect to the broker
client.connect(broker, 1883, 60)

# Subscribe to all specified topics
for topic in topics:
    client.subscribe(topic)

# Set the on_message function to handle incoming messages
client.on_message = on_message

# Start the loop to process incoming and outgoing messages
client.loop_forever()
