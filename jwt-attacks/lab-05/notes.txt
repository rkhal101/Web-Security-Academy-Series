Lab #5 - JWT authentication bypass via jku header injection

Vulnerable parameter - JWT

Goal - Forge a JWT by adding the jku parameter and delete the user carlos

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
1) Check if the JWT signature is verified.
2) Check if the application accepts an unsigned JWT / none algorithm
3) Check for weak signing key / brute-force secret key
4) Check if the application accepts an arbitrary injected jwk parameter
5) Check if the application accepts an arbitrary jku parameter


- Generate our RSA key
- Add the public key in the exploit server
- Modify the JWT to include the jku parameter and the subject administrator
- sign the jwt using the private key 