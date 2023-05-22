from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import serial
import time
import os

# Check if .env file exists and load it
if os.path.exists('.env'):
    load_dotenv()
else:
    print("""
    .env file does not exist.
    Please follow these steps:
    1. Create a new .env file in the same directory as your Python script.
    2. Copy the content of .env.example to .env file.
    3. Change username and password with your own credentials.
    """)
    exit(0)

# Set the serial port and baud rate
serial_port = '/dev/cu.usbmodem1101'
baud_rate = 9600

# Open the serial port
try:
    ser = serial.Serial(serial_port, baud_rate)
except serial.SerialException:
    ser = None
    print(f"""
    Serial port '{serial_port}' is not available or already in use.
    Please follow these steps:
      1. Ensure that your Arduino is plugged in.
      2. Check the port to which it is connected by navigating to Tools > Port in the Arduino IDE.
      3. Close the Arduino IDE to release the port.
    """)
 
    exit(0)

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
door = broker_username+"/door"

# Wait for the Arduino to initialize
time.sleep(2)


def send_command(command):
    if ser is not None:
        ser.write(command.encode())


def on_message(client, userdata, message):
    access_message = str(message.payload.decode("utf-8"))
    print(access_message)
    send_command(access_message)


client.loop_start()

client.subscribe(door)
client.on_message = on_message
time.sleep(300)

client.loop_stop()
