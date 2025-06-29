import websocket
import json
import time
import threading

def mouth_(time_open, time_close):
    mouth_open = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "mouthOpen",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "faceFound": False,
                    "mode": "set",
                    "parameterValues": [
                        {
                            "id": "MouthOpen",
                            "value": 1
                        }
                    ]
                }
            }
    ws.send(json.dumps(mouth_open))
    time.sleep(time_open)

            # Close mouth
    mouth_close = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "mouthClose",
        "messageType": "InjectParameterDataRequest",
        "data": {
            "faceFound": False,
            "mode": "set",
            "parameterValues": [
                {
                    "id": "MouthOpen",
                    "value": 0
                }
            ]
        }
    }
    ws.send(json.dumps(mouth_close))
    time.sleep(time_close)

def mouth_loop(ws):
    try:
        while True:
            mouth_(0.5, 0.5)
    except Exception as e:
        print("Mouth loop stopped:", e)

def on_message(ws, message):
    response = json.loads(message)
    print("Received:", json.dumps(response, indent=2))
    if response.get("messageType") == "AuthenticationResponse" and response["data"].get("authenticated"):
        model_info = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "getModel",
            "messageType": "CurrentModelRequest"
        }
        ws.send(json.dumps(model_info))
    elif response.get("messageType") == "CurrentModelResponse":
        # Start the mouth open/close loop in a background thread
        threading.Thread(target=mouth_loop, args=(ws,), daemon=True).start()

def on_open(ws):
    auth = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "auth",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": "MyCoolPlugin",
            "pluginDeveloper": "MyName",
            "authenticationToken": "0380bfb7214af2c3a9c53101962c542d5a8528acaba4ab30a878f6112df92278"
        }
    }
    ws.send(json.dumps(auth))

ws = websocket.WebSocketApp(
    "ws://localhost:8001",
    on_open=on_open,
    on_message=on_message
)
ws.run_forever()