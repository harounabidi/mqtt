import paho.mqtt.client as mqtt
import streamlit as st
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set up MQTT broker connection
broker_address = "maqiatto.com"
broker_port = 1883
broker_username = os.getenv("BROKER_USERNAME")
broker_password = os.getenv("BROKER_PASSWORD")

# Topics
motor_speed = broker_username+"/motor_speed"

# Define the Streamlit app


def app():

    # MQTT Client
    client = mqtt.Client()
    client.username_pw_set(username=broker_username, password=broker_password)
    client.connect(broker_address)

    # Define the slider widget
    speed = st.slider("Select a value", 0, 100, 50)

    # Publish the speed value
    client.publish(motor_speed, speed)

    # Disconnect from MQTT broker
    client.disconnect()


# Run the Streamlit app
if __name__ == '__main__':
    app()
