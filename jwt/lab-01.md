
# [Lab: JWT authentication bypass via unverified signature](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)

- This lab uses a JWT-based mechanism for handling sessions.
- Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.
- **To solve the lab, modify your session token to gain access to the admin panel at `/admin`.**
- Then delete the user carlos. You can log in to your own account using the following credentials: `wiener:peter`.
---

  </br>

  ## Must edit the user name in the JWT sub claim
  - ### Login as peter, and send the request `GET /my-account?id=wiener` to the repeater
  - ### Highlight the Payload Data section of the JWT
     </br>
 
![jwt-lab-01-jwt-sub-highlite](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/e0faee7b-883b-4a52-ace7-61b8772292a9)

 </br>
 
    
  - ### In the inspector panel, change the username from `"sub":"wiener"`  to `"sub":"administrator"`

 </br>
 
![jwt-lab-01-subclaimchange-02](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/fa10e673-08bb-4650-9bf2-bab29360a384)



 </br>

  - ### Then save changes, change request path from `GET /my-account?id=wiener` to `GET /admin` , and send the request
  - ### This lands you in the administrators panel, and from there, you can search for carlos in the response HTML to find

    `<a href="/admin/delete?username=carlos">`
  - ### Then change the request to `GET /admin/delete?username=carlos `
  - ### Lab solved!
 
    
