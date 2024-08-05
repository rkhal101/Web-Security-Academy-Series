
Lab #2 - JWT authentication bypass via flawed signature verification

Vulnerable parameter - JWT

Goal - modify the session token to gain access to the /admin panel and delete the user carlos

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
1) Check if the JWT signature is verified.
2) Check if the application accepts an unsigned JWT / none algorithm