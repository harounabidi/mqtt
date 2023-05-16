import paho.mqtt.client as mqtt
import time
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set up MQTT broker connection
broker_address = "maqiatto.com"
broker_port = 1883
broker_username = os.getenv("BROKER_USERNAME")
broker_password = os.getenv("BROKER_PASSWORD")

# MQTT Client
client = mqtt.Client()
client.username_pw_set(username=broker_username, password=broker_password)
client.connect(broker_address)

# Topic
motor_speed = broker_username+"/motor_speed"
light = broker_username+"/light"


def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))


client.loop_start()

client.subscribe(motor_speed)
client.on_message = on_message
time.sleep(300)

client.loop_stop()
