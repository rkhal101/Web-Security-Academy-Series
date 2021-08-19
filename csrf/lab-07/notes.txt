Lab #7 - CSRF where Referer validation depends on header being present

Vulnerable parameter - email change functionality

Goal - exploit CSRF to change email address

Creds - wiener:peter

Analysis:

In order for a CSRF attack to be possible:
- A relevant action: change a users email
- Cookie-based session handling: session cookie
- No unpredictable request parameters: no csrf token

Testing Referer header for CSRF attacks:
1. Remove the Referer header