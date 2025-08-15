from flask import Flask, render_template
import subprocess
import platform
import ipaddress

app = Flask(__name__)

# כתובת רשת שלך – שנה לפי הצורך
NETWORK = "192.168.1.0/24"

def scan_network():
    active_devices = []
    param = "-n" if platform.system().lower()=="windows" else "-c"

    for ip in ipaddress.IPv4Network(NETWORK):
        res = subprocess.run(["ping", param, "1", "-w", "1000", str(ip)],
                             stdout=subprocess.DEVNULL)
        if res.returncode == 0:
            active_devices.append(str(ip))
    return active_devices

@app.route("/")
def index():
    devices = scan_network()
    return render_template("index.html", devices=devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
