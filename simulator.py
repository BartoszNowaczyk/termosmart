import time
import random
import json
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=termosmartHub.azure-devices.net;DeviceId=device01;SharedAccessKey=SEIRhMTakvzUT8h1WCJm2JyhEvZNi+fnz2JszBykn9g="

def create_client():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def generate_data():
    return {
        "temperature": round(random.uniform(18.0, 28.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2)
    }

def main():
    client = create_client()
    print("Połączono z Azure IoT Hub")
    while True:
        data = generate_data()
        msg = Message(json.dumps(data)) 
        client.send_message(msg)
        print("Wysłano:", data)
        time.sleep(10)

if __name__ == "__main__":
    main()
