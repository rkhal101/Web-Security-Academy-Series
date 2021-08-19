Lab #3 - CSRF where token validation depends on token being present

Vulnerable parameter - email change functionality

Goal - exploit CSRF to change email address

Creds - wiener:peter

Analysis:

In order for a CSRF attack to be possible:
- A relevant action: change a users email
- Cookie-based session handling: session cookie
- No unpredictable request parameters: csrf token is not mandatory

Testing CSRF Tokens:
1. Remove the CSRF token and see if application accepts request
2. Change the request method from POST to GET
