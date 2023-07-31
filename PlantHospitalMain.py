import websocket
import json
import threading
import time
import requests
import http.client
"""
# system library for getting the command line argument
import sys
# web library
import http.client
def send( message ):
    # your webhook URL
    webhookurl = "https://discordapp.com/api/webhooks/YOURWEBHOOK"
    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"
    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
        })
    # get the response
    response = connection.getresponse()
    result = response.read()
    # return back to the calling function with the result
    return result.decode("utf-8")
# send the messsage and print the response
print( send( sys.argv[1] ) )
"""

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def send_json_message(message):

    webhookurl = "https://discord.com/api/webhooks/1135662267338326017/NuHNa6839rqJHt3esRFxmG5APow7z3aMluMxOmEVjyDyakrAUG_GmfxQrgEb2z5ne0V-"
    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"
    # get the connection and make the request
    connection = http.client.HTTPSConnection("discord.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })

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

heartbeat_interval = event["d"]["heartbeat_interval"] / 10000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
#threading._start_new_thread(test_send_json_request, ())

token = "MzMzMzA4NDYzOTI3MTMyMTcx.G_byfH.ShH73j3rN0-ahjyyu7nH6Avhim5yQjoJ3uN794"
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
            print("should")
            send_json_message("CREAM")

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")

    except:
        pass