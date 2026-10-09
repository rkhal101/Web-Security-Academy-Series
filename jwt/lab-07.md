## [Lab: JWT authentication bypass via algorithm confusion](https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion)

- This lab uses a JWT-based mechanism for handling sessions. 
- It uses a robust RSA key pair to sign and verify tokens. 
- However, due to implementation flaws, 
- this mechanism is vulnerable to algorithm confusion attacks.

- To solve the lab, first obtain the server's public key. 
- This is exposed via a standard endpoint. 
- Use this key to sign a modified session token that gives you access to the admin panel at `/admin`, then delete the user `carlos`.

- You can log in to your own account using the following credentials: `wiener:peter`

**You can assume that the server stores its public key as an X.509 PEM file**

---
#### But first, a note on X.509 PEM format in regards to JSON Web Tokens

X.509 PEM format and JSON Web Tokens (JWTs) are two different standards used in digital communication, often in the context of authentication and security, but they serve different purposes.

1. **X.509 PEM Format**:
   - X.509 is a standard defining the format of public key certificates. These certificates are used in many Internet protocols to ensure the authenticity of an entity's identity.
   - PEM (Privacy Enhanced Mail) is a format for storing and transmitting cryptographic keys, certificates, and other data, often used in X.509 certificates. It's a base64-encoded ASCII format with delimiters like `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`.
   - In the context of X.509 certificates, the PEM format is commonly used to encode the public key certificate, private key, and other related information.

2. **JSON Web Tokens (JWTs)**:
   - JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed.
   - JWTs consist of three parts separated by dots: a header, a payload, and a signature. These parts are base64-encoded JSON objects.
   - JWTs are commonly used for authentication and information exchange between parties, typically in web applications and APIs.

Now, regarding the connection between X.509 PEM format and JWTs:

- X.509 certificates can be used to sign JWTs. This means that the signature part of the JWT (the third part) is generated using the private key corresponding to the X.509 certificate's public key.
- In some authentication scenarios, JWTs are signed using asymmetric cryptography, where the server holds the private key and the client or other parties can verify the signature using the public key.
- The public key for verification can be distributed in various ways, and one common way is through X.509 certificates, often encoded in PEM format.

In summary, X.509 PEM format is not directly related to the structure or content of JWTs. Instead, X.509 certificates in PEM format can be used to provide the public key needed to verify the signature of JWTs, thus enhancing the security of JWT-based authentication systems.

## Performing an algorithm confusion attack

An algorithm confusion attack generally involves the following high-level steps:

1. [Obtain the server's public key](https://portswigger.net/web-security/jwt/algorithm-confusion#step-1-obtain-the-server-s-public-key)
    
2. [Convert the public key to a suitable format](https://portswigger.net/web-security/jwt/algorithm-confusion#step-2-convert-the-public-key-to-a-suitable-format)
    
3. [Create a malicious JWT](https://portswigger.net/web-security/jwt/algorithm-confusion#step-3-modify-your-jwt) with a modified payload and the `alg` header set to `HS256`.
    
4. [Sign the token with HS256](https://portswigger.net/web-security/jwt/algorithm-confusion#step-4-sign-the-jwt-using-the-public-key), using the public key as the secret.
    

In this section, we'll walk through this process in more detail, demonstrating how you can perform this kind of attack using Burp Suite.

### Step 1 - Obtain the server's public key

Servers sometimes expose their public keys as JSON Web Key (JWK) objects via a standard endpoint mapped to `/jwks.json` or `/.well-known/jwks.json`, for example. These may be stored in an array of JWKs called `keys`. This is known as a JWK Set.

`{ "keys": [ { "kty": "RSA", "e": "AQAB", "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab", "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ" }, { "kty": "RSA", "e": "AQAB", "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA", "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw" } ] }`

Even if the key isn't exposed publicly, you may be able to [extract it from a pair of existing JWTs](https://portswigger.net/web-security/jwt/algorithm-confusion#deriving-public-keys-from-existing-tokens).

### Step 2 - Convert the public key to a suitable format

Although the server may expose their public key in JWK format, when verifying the signature of a token, it will use its own copy of the key from its local filesystem or database. This may be stored in a different format.

In order for the attack to work, the version of the key that you use to sign the JWT must be identical to the server's local copy. In addition to being in the same format, every single byte must match, including any non-printing characters.

For the purpose of this example, let's assume that we need the key in X.509 PEM format. You can convert a JWK to a PEM using the [JWT Editor](https://portswigger.net/bappstore/26aaa5ded2f74beea19e2ed8345a93dd) extension in Burp as follows:

1. With the extension loaded, in Burp's main tab bar, go to the **JWT Editor Keys** tab.
    
2. Click **New RSA** Key. In the dialog, paste the JWK that you obtained earlier.
    
3. Select the **PEM** radio button and copy the resulting PEM key.
    
4. Go to the **Decoder** tab and Base64-encode the PEM.
    
5. Go back to the **JWT Editor Keys** tab and click **New Symmetric Key**.
    
6. In the dialog, click **Generate** to generate a new key in JWK format.
    
7. Replace the generated value for the `k` parameter with a Base64-encoded PEM key that you just copied.
    
8. Save the key.
    

### Step 3 - Modify your JWT

Once you have the public key in a suitable format, you can [modify the JWT](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#editing-jwts) however you like. Just make sure that the `alg` header is set to `HS256`.

### Step 4 - Sign the JWT using the public key

[Sign the token](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#adding-a-jwt-signing-key) using the HS256 algorithm with the RSA public key as the secret.
---

# Solving the lab - just follow the generic insrtuctions from the lesson


### Step 1 - Obtain the server's public key
log in and send a req to repeater then send a get req to `/jwks.json`

```http
GET /jwks.json
```

![Screenshot_20240321_174822](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/510cfa8e-ad1a-467c-abf1-79c7c28937f4)

#### you want to copy the JWK object from the response, but what part is it exactly?

#### it's the contents between the opening `{` and the closing `}`


![Screenshot_20240321_183039](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/d226b7cf-0297-436c-9abd-a15e0575ae39)


##### Part 2 - Generate a malicious signing key
 In Burp, go to the **JWT Editor Keys** tab in Burp's main tab bar.
    
Click **New RSA Key**.
    
In the dialog, make sure that the **JWK** option is selected, then paste the JWK that you just copied. Click **OK** to save the key.


![Screenshot_20240321_183357](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/009a5781-f8c3-4f83-8d3c-2283ab05c417)


Right-click on the entry for the key that you just created, then select **Copy Public Key as PEM**.



![Screenshot_20240321_183434](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/1bec9b91-1f87-4e73-a5ec-f4925ef9a723)



Use the **Decoder** tab to Base64 encode this PEM key, then copy the resulting string.





![Screenshot_20240321_183606](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/c791c01e-5729-42ac-8cdf-3d68f260ba4e)



Go back to the **JWT Editor Keys** tab in Burp's main tab bar.

Click **New Symmetric Key**. In the dialog, click **Generate** to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.

![Screenshot_20240321_183738](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/53b45660-3838-4cf2-8050-42929cb9bc60)


Replace the generated value for the k property with a Base64-encoded PEM that you just created.

![Screenshot_20240321_183814](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/3537e41c-ae6d-4d2c-8773-fcca75e0cbef)



Save the key.


##### Part 3 - Modify and sign the token

 Go back to the `GET /admin` request in Burp Repeater and switch to the extension-generated **JSON Web Token** tab.

In the header of the JWT, change the value of the `alg` parameter to `HS256`.
and
In the payload, change the value of the `sub` claim to `administrator`.

![Screenshot_20240321_184158](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/5846b4fe-8f7f-4161-b10f-fbcddd7dcb00)


At the bottom of the tab, click **Sign**, then select the symmetric key that you generated in the previous section.
![Screenshot_20240321_184256](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/3e5ab816-6faf-47c5-b4a6-089a86f07663)



Make sure that the **Don't modify header** option is selected, then click **OK**. The modified token is now signed using the server's public key as the secret key.





Send the request and observe that you have successfully accessed the admin panel.

In the response, find the URL for deleting `carlos` (`/admin/delete?username=carlos`). Send the request to this endpoint to solve the lab.

![Screenshot_20240321_184324](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/b7b592ed-3706-4068-ab9a-531874d12e74)


##### BOOM! Lab solved

