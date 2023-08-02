import websocket
import json
import threading
import time
import requests
import http.client

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def send_json_message(message):

    webhookurl = "https://discord.com/api/webhooks/1135662267338326017/NuHNa6839rqJHt3esRFxmG5APow7z3aMluMxOmEVjyDyakrAUG_GmfxQrgEb2z5ne0V-"

    data = {"content": message}
    response = requests.post(webhookurl, json=data)

    print(response.status_code)

    print(response.content)



def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print("Heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null",
        }

        send_json_request(ws, heartbeatJSON)
        print("Heartbeat Sent")

ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
event = receive_json_response(ws)

#heartbeat_interval = event["d"]["heartbeat_interval"] / 20000
#threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
#threading._start_new_thread(test_send_json_request, ())

token = "MTEzNTc3MDAyMTU0NTY2MDUwNw.Gl5Wza.HdfeodN8Aa4MnhMVNnpVayOorMxibdU23eseyo"
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

send_json_request(ws, payload)

while True:


    try:

        event = receive_json_response(ws)

        response = f"{event['d']['content']}"
        print(response)

        if response.startswith("ICE"):
            send_json_message("CREAM")

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")

    except websocket._exceptions.WebSocketConnectionClosedException:
        print("Restarting Server")
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=6&encording=json")

        event = receive_json_response(ws)

        send_json_request(ws, payload)

        pass

    except:

        pass