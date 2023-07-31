import websocket
import json
import threading
import time
import requests

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def send_json_message(message, token, channelid):
    payload = {
        "content": message
    }

    headers = {
        "authorization": token
    }

    r = requests.post(f"https://discord.com/api/v8/channels/{channelid}/messages", headers=headers, data=payload)

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

heartbeat_interval = event["d"]["heartbeat_interval"] / 5000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
#threading._start_new_thread(test_send_json_request, ())

token = "MzMzMzA4NDYzOTI3MTMyMTcx.X-wv-w.jc9TJJv01ubtdXdn-rzauAkgMVA"
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
    event = receive_json_response(ws)

    try:
        response = f"{event['d']['content']}"
        print(response)

        if response.startswith("ICE"):
            send_json_message("CREAM", token, "1135657445532909621")

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")

    except:
        pass