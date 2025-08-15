# main.py
from flask import Flask, render_template, request
import websocket
import json

app = Flask(__name__)

# כתובת IP של הטלוויזיה
TV_IP = "192.168.1.50"
PORT = 8001
WS_URL = f"ws://{TV_IP}:{PORT}/api/v2/channels/samsung.remote.control"

def send_command(command):
    try:
        ws = websocket.WebSocket()
        ws.connect(WS_URL)
        payload = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": command,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        }
        ws.send(json.dumps(payload))
        ws.close()
        return True
    except Exception as e:
        print("שגיאה בשליחת פקודה:", e)
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    cmd = request.form.get("cmd")
    success = send_command(cmd)
    return "OK" if success else "ERROR"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
