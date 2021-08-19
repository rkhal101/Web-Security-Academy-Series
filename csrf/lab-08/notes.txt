Lab #8 - CSRF where token is duplicated in cookie

Vulnerable parameter - email change functionality

Goal - exploit CSRF to change email address

Creds - wiener:peter

Analysis:

In order for a CSRF attack to be possible:
- A relevant action: change a users email
- Cookie-based session handling: session cookie
- No unpredictable request parameters (satisfied b/c no csrf token)

Testing Referer header for CSRF attacks:
1. Remove the Referer header
2. Check which portion of the referrer header is the application validating