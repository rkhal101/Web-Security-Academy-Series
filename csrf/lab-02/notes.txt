Lab #2 - CSRF where token validation depends on request method

Vulnerable parameter - email change functionality

Goal - exploit CSRF to change email address

Creds - wiener:peter

Analysis:

In order for a CSRF attack to be possible:
- A relevant action: change a users email
- Cookie-based session handling: session cookie
- No unpredictable request parameters: Request method can be changed to GET which does not require CSRF token

Testing CSRF Tokens:
1. Change the request method from POST to GET
