# MaQiaTTo online broker python script

This repository contains a Python script for interacting with the MaQiaTTo online broker. Follow the instructions below to set up and use the script.

## How to use

1. Create MaQiaTTo account at [maqiatto.com](https://www.maqiatto.com/).
2. Create the necessary topics. For example, you can create a topic named "door" (the provided example assumes this topic exists).

### Clone the Repository

```
git clone https://github.com/harounabidi/mqtt.git
```

or download [here](https://github.com/harounabidi/mqtt/archive/refs/heads/main.zip)

### Install requirements

Install the required Python packages by running the following command:

```
pip install -r requirements.txt
```

## Configure .env File

1. Copy the contents of `.env.example` file.
2. Create a new file named `.env`.
3. Paste the copied contents into the `.env` file.
4. Replace the placeholders with your actual MaQiaTTo credentials. Replace `username` with your MaQiaTTo username and `password` with your MaQiaTTo password.

Example .env file:

```
BROKER_USERNAME=your_username
BROKER_PASSWORD=your_password
```

### Publisher

To publish messages to a topic using a web interface, run the following command:

```
python mqtt_publish.py
```

### Subscriber

To subscribe to a topic and receive messages, run the following command:

```
python mqtt_subscriber.py
```

This will execute the `mqtt_subscriber.py` script and listen for incoming messages on the subscribed topic.

Feel free to reach out if you have any further questions or issues.
