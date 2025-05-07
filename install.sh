#!/bin/bash

set -e

echo "[*] Updating system and installing packages..."
sudo apt-get update
sudo apt-get install -y hostapd dnsmasq python3-flask

echo "[*] Disabling hostapd and dnsmasq for now..."
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

echo "[*] Creating directories..."
sudo mkdir -p /opt/wifi-setup
sudo cp config.html /opt/wifi-setup/
sudo cp wifi_check.py /opt/wifi-setup/
sudo cp wifi-setup.service /etc/systemd/system/


[ -f /etc/hostapd/hostapd.conf ] && sudo rm /etc/hostapd/hostapd.conf
sudo cp hostapd.conf /etc/hostapd/

[ -f /etc/dnsmasq.conf ] && sudo rm /etc/dnsmasq.conf
sudo cp dnsmasq.conf /etc/

echo "[*] Enabling systemd service..."
sudo systemctl enable wifi-setup

echo "[*] Done. Rebooting..."
sudo reboot
