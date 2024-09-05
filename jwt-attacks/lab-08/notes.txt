Lab #8 - JWT authentication bypass via algorithm confusion with no exposed key

Vulnerable parameter - JWT

Goal - modify and sign the JWT and delete the user carlos

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
1) Check if the JWT signature is verified.
2) Check if the application accepts an unsigned JWT / none algorithm
3) Check for weak signing key / brute-force secret key
4) Check if the application accepts an arbitrary injected jwk header
5) Check if the application accepts an arbitrary jku header
6) Check if the kid parameter is vulnerable to path traversal.
7) Check if the application is vulnerable to algorithm confusion.

1 - Symmetric algorithm - one key
2 - Asymmetric algorithms - 2 keys
    - sign token / private key
    - verify token / public key