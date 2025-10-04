# Kortex Shield: Fail2ban Integration Guide

This guide explains how to integrate Fail2ban with Kortex Shield to automatically block malicious IP addresses, turning your detection system into a prevention system. This setup is performed on the **host machine** running Docker.

## Step 1: Install Fail2ban
On a Debian-based system like Ubuntu, install Fail2ban:
```bash
sudo apt-get update
sudo apt-get install fail2ban

[Definition]
failregex = {"timestamp": ".*", "client_ip": "<HOST>", "score": .*, "payload": ".*"}
ignoreregex =

[kortex-shield]
enabled  = true
port     = http,https
filter   = kortex-shield
logpath  = /path/to/your/kortex-shield/detections/detections.log  # IMPORTANT: Use the full, absolute path
maxretry = 3
findtime = 10m
bantime  = 1h

