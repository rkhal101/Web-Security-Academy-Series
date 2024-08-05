Lab #3 - JWT authentication bypass via weak signing key

Vulnerable parameter - JWT

Goal - Brute-force the website's secret key, use it to craft an administrator JWT and delete the user carlos.

creds - wiener:peter

Analysis:

Testing for JWT vulnerabilities:
1) Check if the JWT signature is verified.
2) Check if the application accepts an unsigned JWT / none algorithm
3) Check for weak signing key / brute forcable secret key (symmetric)