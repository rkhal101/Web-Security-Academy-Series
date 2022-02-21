Lab #3 - CORS vulnerability with trusted insecure protocols

Target Goal - exploit the CORS misconfiguration to retrieve the administrator's API key

Creds - wiener:peter

Analysis:

Testing for CORS misconfigurations:
1. Change the origin header to an arbitrary value
2. Change the origin header to the null value
3. Change the origin header to one that begins with the origin of the site.
4. Change the origin header to one that ends with the origin of the site.