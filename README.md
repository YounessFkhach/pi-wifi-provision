# 📡 Raspberry Pi Wi-Fi Provisioning System

This project enables a Raspberry Pi (Zero or 4) to automatically boot into a configuration mode if it fails to connect to Wi-Fi. In configuration mode, it creates a Wi-Fi hotspot with a web portal where users can enter their home network credentials. Once submitted, the Pi connects to the Wi-Fi network.

## 🔧 Features

    Auto-starts a Wi-Fi hotspot when not connected

    Web interface to configure Wi-Fi credentials

    Supports WPA/WPA2 and open networks

    Works with NetworkManager

    Automatic fallback to hotspot if connection fails

    Built-in service control and connection validation

## ⚙️ How It Works

    Boot sequence begins

    The system checks for an existing Wi-Fi connection:

        If connected → continues normal operation.

        If not connected → starts AP mode.

    Access Point (AP) mode:

        Hostname: Pi_Config_AP

        IP address: 10.0.0.1

        Visit http://10.0.0.1 in your browser.

    Enter Wi-Fi details and submit.

    The Pi connects to your Wi-Fi. If it fails, it returns to AP mode.

## 🚀 Installation

On a fresh Raspberry Pi OS with NetworkManager:

git clone https://github.com/YounessFkhach/pi-wifi-provision.git
cd pi-wifi-provision
chmod +x install.sh
sudo ./install.sh

    📌 The script sets up all necessary services, dependencies, and restarts the device.

## 🌐 Web Interface

The configuration form is mobile-friendly and modern:

    📶 SSID input

    🔐 Encryption type selector

    🔑 Password field

Access it via http://10.0.0.1 when in configuration mode.
