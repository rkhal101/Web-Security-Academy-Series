Lab #8 - User ID controlled by request parameter, with unpredictable user IDs

Target Goal - Find the GUID for carlos and compromise his account

creds: wiener:peter

Steps to exploit:

1. Log into the wiener account
2. Loop through all the posts and identify which one is written by the carlos user
3. Extract the GUID
4. Access the Carlos user account
5. Extract the API key of Carlos.