Lab #2 - Basic SSRF against another back-end system

Vulnerable feature - stock check functionality

Goal -  use the stock check functionality to scan the internal 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos. 

Analysis:

application running on: http://192.168.0.190:8080/admin

delete carlos: http://192.168.0.190:8080/admin/delete?username=carlos

python3 script.py <url>

192.168.0.255