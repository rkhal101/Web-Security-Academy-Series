Lab #4 - JWT authentication bypass via jwk header injection

Vulnerable parameter - JWT

Goal - modify and sign the JWT and delete the user carlos

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
1) Check if the JWT signature is verified.
2) Check if the application accepts an unsigned JWT / none algorithm
3) Check for weak signing key / brute-force secret key (symmetric)
4) Check if the application accepts an arbitrary injected jwk header / jwk injection (public-key)