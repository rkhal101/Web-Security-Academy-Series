Lab #4 - CSRF where token is not tied to user session

Vulnerable parameter - email change functionality

Goal - exploit CSRF to change email address

Credentials - wiener:peter, carlos:montoya

Analysis:

In order for a CSRF attack to be possible:
- A relevant action: change a users email
- Cookie-based session handling: session cookie
- No unpredictable request parameters: csrf token is not tied to user session

Testing CSRF Tokens:
1. Remove the CSRF token and see if application accepts request
2. Change the request method from POST to GET
3. See if csrf token is tied to user session