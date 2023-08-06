import websocket
import json
from threading import Thread
import time
import requests
import http.client


class PlantHospital():

    def __init__(self, ws):
        self.delay = 1
        self.name = "Plant"
        self.thirst_bound = 1
        self.ws = ws

        self.cycle = True

        self.thread = Thread(target=self.thirst_wait)
        self.thread.start()

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = float(delay)
        self.cycle = False
        self.thread.join()
        self.cycle = True
        self.thread = Thread(target=self.thirst_wait)
        self.thread.start()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_thirst(self):
        return self.thirst_bound

    def set_thirst(self, thirst):
        self.thirst_bound = float(thirst)

    def thirst_reporting(self):
        return 2

    def thirst_wait(self):
        start_time = time.time()
        while self.cycle:
            current_time = time.time()
            if (current_time - start_time) > (self.get_delay() * 3600):
                start_time = time.time()
                self.send_json_message("My current thirst level is " + str(self.thirst_reporting()))

    def send_json_request(self, request):
        self.ws.send(json.dumps(request))

    def send_json_message(self, message):

        webhookurl = "https://discord.com/api/webhooks/1135662267338326017/NuHNa6839rqJHt3esRFxmG5APow7z3aMluMxOmEVjyDyakrAUG_GmfxQrgEb2z5ne0V-"

        data = {"content": message}
        response = requests.post(webhookurl, json=data)

    def receive_json_response(self):
        response = self.ws.recv()
        if response:
            return json.loads(response)

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")

planthospital = PlantHospital(ws)

event = planthospital.receive_json_response()

#heartbeat_interval = event["d"]["heartbeat_interval"] / 20000
#threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
#threading._start_new_thread(test_send_json_request, ())

token = "MTEzNTc3MDAyMTU0NTY2MDUwNw.GG8OjP.ujOCpVaJjrj3X5UYBZScmopKdGsJBnVKv6sFgs"
payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

planthospital.send_json_request(payload)

#threading._start_new_thread(thirst_wait, (planthospital))


while True:


    try:

        event = planthospital.receive_json_response()

        response = f"{event['d']['content']}"
        print(response)

        if response.startswith("NAME"):
            planthospital.set_name(response.split(": ")[1])
            planthospital.send_json_message("My name is now " + planthospital.get_name())

        if response.startswith("DELAY"):
            planthospital.set_delay(response.split(": ")[1])
            planthospital.send_json_message("My reporting delay is now " + str(planthospital.get_delay()) + " hours")

        if response.startswith("THIRST"):
            planthospital.set_thirst(response.split(": ")[1])
            planthospital.send_json_message("My reporting thirst level is now " + str(planthospital.get_thirst()))

        if response.startswith("GET"):
            if response.split(": ")[1] == "NAME":
                planthospital.send_json_message("My name is " + planthospital.get_name())
            if response.split(": ")[1] == "DELAY":
                planthospital.send_json_message("My reporting delay is " + str(planthospital.get_delay()) + " hours")
            if response.split(": ")[1] == "THIRST":
                planthospital.send_json_message("My reporting thirst level is " + str(planthospital.get_thirst()))

        if response.startswith("STATUS"):
            planthospital.send_json_message("My current thirst reading is " + str(planthospital.thirst_reporting()))

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")

    except websocket._exceptions.WebSocketConnectionClosedException:
        print("Restarting Server")
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=6&encording=json")

        planthospital.ws = ws

        event = planthospital.receive_json_response()

        planthospital.send_json_request(payload)

        pass

    except Exception as e:

        print(e)

        pass