Lab #1 - JWT authentication bypass via unverified signature

Vulnerable parameter - JWT

Goal - modify the session token to gain access to the /admin panel and delete the user carlos

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
- Check if the JWT signature is verified