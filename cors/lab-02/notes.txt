Lab #2 - CORS vulnerability with trusted null origin

Target Goal - exploit the CORS misconfiguration to retrieve the administrator's API key

Creds - wiener:peter

Analysis:

Testing for CORS misconfigurations:
1. Change the origin header to an arbitrary value
2. Change the origin header to the null value
3. 