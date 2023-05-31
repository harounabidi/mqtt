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
    print("Serial connection established successfully")
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
broker_username = os.getenv("BROKER_USERNAME")  # Get username from .env file
broker_password = os.getenv("BROKER_PASSWORD")  # Get password from .env file

# Broker topics
door = broker_username+"/door"

# MQTT Client
client = mqtt.Client()
client.username_pw_set(username=broker_username, password=broker_password)
client.connect(broker_address)


# Wait for the Arduino to initialize
time.sleep(2)


def send_command(command):
    if ser is not None:
        ser.write(command.encode())


def read_response():
    if ser is not None:
        try:
            # Read response from arduino (Serial.println() messages)
            response = ser.readline().decode().strip()
            return response
        except serial.SerialException:
            print("Serial port disconnected, Exiting...")
            exit(0)


def setup():
    # Start the setup
    send_command('S')

    # Wait for the Arduino to complete setup
    response = read_response()
    print('Arduino setup done')
    while response != 'Setup done':
        response = read_response()


def loop():
    while True:
        response = read_response()
        client.publish(door, response)


def close_serial_port():
    if ser is not None:
        ser.close()


# Main execution
try:
    setup()
    loop()
except KeyboardInterrupt:
    pass
finally:
    close_serial_port()
