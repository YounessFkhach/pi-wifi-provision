#!/usr/bin/env python3

import os
import time
import subprocess
import flask
from flask import request

app = flask.Flask(__name__)
config_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
ap_ssid = "Pi_Config_AP"
ap_ip = "10.0.0.1"
disable_flag = "/opt/wifi-setup/disabled.flag"

def is_connected():
    try:
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True)
        return result.stdout.strip() != ""
    except:
        return False

def start_ap():
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl unmask hostapd")
    os.system("sudo systemctl enable hostapd")
    os.system("sudo systemctl stop hostapd")
    os.system("sudo ip link set wlan0 down")
    os.system("sudo ip link set wlan0 up")
    os.system("sudo ip addr add 10.0.0.1/24 dev wlan0")
    os.system("sudo systemctl start dnsmasq")
    os.system("sudo systemctl start hostapd")

def stop_ap():
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo ip addr flush dev wlan0")
    os.system("sudo wpa_cli -i wlan0 reconfigure")

def write_wifi_config(ssid, encryption, password):
    net_block = f"""
network={{
    ssid="{ssid}"
    key_mgmt={encryption}
    psk="{password}"
}}
"""
    with open(config_file, "w") as f:
        f.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        f.write("update_config=1\n")
        f.write(net_block)

@app.route('/', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        ssid = request.form.get('ssid')
        encryption = request.form.get('encryption', 'WPA-PSK')
        password = request.form.get('password')
        write_wifi_config(ssid, encryption, password)

        stop_ap()

        # Use NetworkManager to connect
        connect_cmd = f"nmcli device wifi connect '{ssid}' password '{password}'"
        os.system(connect_cmd)

        time.sleep(20)

        if not is_connected():
            start_ap()
        return "Configuration saved. Trying to connect..."
    return flask.send_file("config.html")

if __name__ == '__main__':
    stop_ap()
    if os.path.exists(disable_flag):
        print("Setup is disabled (disabled.flag present).")
        exit(0)

    time.sleep(30)
    if not is_connected():
        start_ap()
        app.run(host=ap_ip, port=80)
