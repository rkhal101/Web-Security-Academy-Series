Lab #4 - CORS vulnerability with internal network pivot attack

Target Goals:
1. Use JS to locate an endpoint on the local network (192.168.0.0/24 port 8080)
2. Exploit CORS misconfiguration to delete user Carlos.

Analysis:

Steps to complete the exercise:
1. Scan the local network (192.168.0.0/24) for endpoints that have port 8080 open.
Completed - http://192.168.0.181:8080

2. Try to find an XSS vulnerability in the login page
Completed - username field vulnerable to XSS.

3. Use the XSS vulnerability in order to access an authenticated page.
Completed - accessed the admin page.

4. Use XSS vulnerability to delete the Carlos user. 
