# Kortex Shield: System Architecture

## Overview
Kortex Shield is an adaptive, AI-powered Web Application Firewall (WAF) that uses a Transformer model to detect anomalous web requests. It is designed for non-blocking analysis and includes an optional integration with Fail2ban to evolve from an Intrusion Detection System (IDS) into a full Intrusion Prevention System (IPS).

## Core Components
1.  **Nginx (Reverse Proxy & Mirror)**: The public entry point. It uses the `mirror` directive to send an asynchronous copy of every request to the `kortex-shield` API for analysis.
2.  **Tomcat Applications**: The backend web applications being protected.
3.  **Kortex Shield API (Inference Service)**: The AI "brain". It receives mirrored requests, normalizes/decodes them, calculates an anomaly score, and logs malicious requests to `detections.log`.
4.  **AI Pipeline (Offline Components)**: Scripts to generate traffic, parse logs, normalize/decode payloads, and train the model. Includes a `fine_tune` script for continuous learning.
5.  **Dashboard**: A Flask-based web UI that provides a real-time view of the `detections.log` file.
6.  **Fail2ban (Intrusion Prevention)**: An optional host-level service that monitors `detections.log` and uses the system firewall to block IPs that trigger repeated alerts.

## Traffic & Blocking Flow
`User` -> `Nginx` -> `Tomcat App` (Immediate Response)
   |
   +--> (Mirrored Copy) --> `Kortex Shield API` --> `detections.log`
                                                       |
                                                       +--> `Dashboard` (reads log for display)
                                                       |
                                                       +--> `Fail2ban` (reads log for blocking) --> **Updates Host Firewall**

This architecture creates a passive detection system that feeds both a real-time monitoring dashboard and an active prevention system, providing intelligent security without compromising performance.
