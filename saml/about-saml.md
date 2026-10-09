# What is SAML?
SAML (Security Assertion Markup Language) is like a digital "hall pass" that
websites use to let you log in without creating a new account. For example, if
you log in to a third-party site using your Google account, SAML is one of the
technologies that might be used to make that happen. It works by sending a
little file (called a "SAML assertion") from your Google account to the
third-party site saying, "Yep, this person is allowed to log in."

---

### **What is SAML?**

**Security Assertion Markup Language (SAML)** is an **XML-based protocol** used for Single Sign-On (SSO) authentication and authorization. It allows users to log into multiple applications using a single set of credentials. SAML works by exchanging authentication data (called **assertions**) between two parties:

1. **Identity Provider (IdP):** The entity that verifies a user's identity (e.g., Google, Okta).
2. **Service Provider (SP):** The application that a user wants to access (e.g., a corporate app).

---

### **How SAML Works**

SAML facilitates **SSO** through a series of steps:

1. **User Request**: A user attempts to access a Service Provider (SP) that requires authentication.
2. **Redirect to IdP**: If the user isn’t authenticated, the SP redirects them to the Identity Provider (IdP).
3. **Authentication at IdP**: The IdP authenticates the user (e.g., via username/password or other methods).
4. **SAML Assertion**: The IdP generates a signed **SAML assertion** (XML document) that contains:
    - **Authentication** details.
    - **Attributes** (e.g., username, roles, or permissions).
5. **Send Assertion**: The SAML assertion is sent back to the SP.
6. **Validation and Access**: The SP validates the assertion (e.g., checks the signature) and grants access.

---

### **Example SAML Assertion**

A **SAML assertion** is an XML document. Here's an example of a SAML response:

```xml
<SAMLResponse>
  <Assertion xmlns="urn:oasis:names:tc:SAML:2.0:assertion">
    <Subject>
      <NameID>user@example.com</NameID>
    </Subject>
    <AttributeStatement>
      <Attribute Name="username" Format="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified">
        <AttributeValue>user123</AttributeValue>
      </Attribute>
      <Attribute Name="role">
        <AttributeValue>admin</AttributeValue>
      </Attribute>
    </AttributeStatement>
    <Conditions NotBefore="2024-06-01T00:00:00Z" NotOnOrAfter="2024-06-02T00:00:00Z" />
    <Signature>
      <!-- Signed by IdP -->
    </Signature>
  </Assertion>
</SAMLResponse>
```

- `NameID`: The user’s unique identifier.
- `AttributeStatement`: Contains attributes about the user (e.g., username, roles).
- `Conditions`: Defines the time validity of the assertion.
- `Signature`: Ensures the integrity and authenticity of the assertion.

---

### **SAML Vulnerabilities and Exploits**

SAML, if **misconfigured or implemented poorly**, can lead to critical vulnerabilities:

---

### **1. XML Signature Wrapping (XSW) Attack**

**What is it?**  
An attacker wraps a **malicious assertion** inside the original XML document to bypass signature verification.

**How it works:**  
1. The application verifies the **signature** on the original (legitimate) assertion.
2. The attacker **injects a second assertion** that is processed later by the application, granting unauthorized access.

---

**Example of an XSW Attack:**

1. Legitimate SAML Response:
   ```xml
   <SAMLResponse>
     <Assertion ID="123">
       <Signature>ValidSignature</Signature>
       <Subject>
         <NameID>user@example.com</NameID>
       </Subject>
     </Assertion>
   </SAMLResponse>
   ```

2. Modified SAML Response (Malicious):
   ```xml
   <SAMLResponse>
     <Assertion ID="123">
       <Signature>ValidSignature</Signature>
       <Subject>
         <NameID>user@example.com</NameID>
       </Subject>
     </Assertion>
     <!-- Malicious Assertion Injected -->
     <Assertion>
       <Subject>
         <NameID>admin@example.com</NameID>
       </Subject>
     </Assertion>
   </SAMLResponse>
   ```

- The **Signature** validates the first assertion, but the SP processes the **second malicious assertion** that grants access as "admin."

**Mitigation:**
- Ensure that SAML implementations strictly **verify signatures** and only process the signed assertion.

---

### **2. SAML Signature Bypass**

**What is it?**  
If a Service Provider fails to validate the **digital signature** properly, an attacker can modify the assertion.

**Exploitation Example:**

Original **Signed** Assertion:
```xml
<Assertion>
  <Subject>
    <NameID>user@example.com</NameID>
  </Subject>
</Assertion>
```

Modified (Unsigned) Assertion:
```xml
<Assertion>
  <Subject>
    <NameID>admin@example.com</NameID>
  </Subject>
</Assertion>
```

If the SP **does not enforce signature verification**, the attacker’s modified assertion grants unauthorized access.

**Mitigation:**
- Always verify digital signatures on SAML assertions.
- Reject unsigned or tampered assertions.

---

### **3. XML External Entity (XXE) in SAML**

**What is it?**  
If the SAML parser is **vulnerable to XXE**, an attacker can inject an external entity to read sensitive files or perform SSRF.

**Example Exploit:**
```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<SAMLResponse>
  <Assertion>
    <Subject>
      <NameID>&xxe;</NameID>
    </Subject>
  </Assertion>
</SAMLResponse>
```

If the XML parser processes the entity, it can leak the contents of `/etc/passwd` back to the attacker.

**Mitigation:**
- Disable external entity processing in XML parsers.
- Use secure libraries for SAML parsing.

---

### **4. Replay Attack**

**What is it?**  
An attacker reuses a **valid SAML response** to gain access.

**How it works:**
1. The attacker captures a valid SAML response (e.g., using a proxy tool like Burp Suite).
2. The same response is replayed to the SP, gaining access.

**Mitigation:**
- Use **one-time tokens** or **timestamps** (`Conditions` tag) to invalidate replayed assertions.
- Implement anti-replay mechanisms on the server.

---

### **5. Misconfigured SAML Assertions**

**What is it?**  
If an SP does not validate the **Conditions** or **Audience** fields, an attacker can reuse assertions across services or extend their validity.

**Example:**

Modified Conditions:
```xml
<Conditions NotBefore="2024-01-01T00:00:00Z" NotOnOrAfter="2026-01-01T00:00:00Z" />
```

- The attacker extends the **NotOnOrAfter** date to keep the assertion valid indefinitely.

**Mitigation:**
- Validate the `NotBefore` and `NotOnOrAfter` timestamps.
- Ensure the `Audience` field matches the intended service.

---

### **Tools to Test SAML Vulnerabilities**

1. **Burp Suite**: Intercept and modify SAML assertions.
2. **SAML Raider**: Burp Suite extension for SAML testing.
3. **Metasploit**: Some modules test for SAML-related flaws.
4. **OWASP ZAP**: Proxy tool for testing web application vulnerabilities.

---

### **Summary**

- SAML provides **Single Sign-On (SSO)** functionality but can be vulnerable to **XML Signature Wrapping**, **Signature Bypass**, **XXE**, **Replay Attacks**, and misconfigurations.
- Exploiting SAML typically involves modifying assertions, injecting entities, or bypassing validation steps.
- Mitigation involves **strict signature validation**, disabling XXE, checking timestamps (`Conditions`), and implementing anti-replay protections.



## **SAML vs OAuth: Comparing Authentication & Authorization Protocols**

Both **SAML** and **OAuth** are widely used for managing authentication and authorization in modern web applications, but they differ in their design, purpose, and use cases.

---

### **What Are SAML and OAuth?**

1. **SAML (Security Assertion Markup Language):**  
   - XML-based protocol used primarily for **Single Sign-On (SSO)** and **authentication**.
   - SAML exchanges XML-based **assertions** between an **Identity Provider (IdP)** and a **Service Provider (SP)** to verify the user’s identity.

2. **OAuth (Open Authorization):**  
   - Token-based protocol designed for **authorization**, allowing applications to access a user’s resources (e.g., APIs, data) without sharing credentials.
   - OAuth uses **access tokens** to grant limited access.

---

### **Key Differences Between SAML and OAuth**

| **Aspect**          | **SAML**                                                     | **OAuth**                                                                                |
| ------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Purpose**         | Focuses on **authentication** (verifying who you are).       | Focuses on **authorization** (granting access to resources).                             |
| **Data Format**     | XML-based (verbose and complex).                             | JSON-based (lightweight, easy to parse).                                                 |
| **Token/Assertion** | SAML Assertion (XML document).                               | Access Token (JSON Web Token - JWT).                                                     |
| **Use Case**        | SSO (Single Sign-On) for enterprise applications.            | Granting permissions for third-party API access.                                         |
| **Protocol Flow**   | Requires redirecting the user to an Identity Provider (IdP). | Direct communication between client and authorization server.                            |
| **Participants**    | - Identity Provider (IdP) <br> - Service Provider (SP)       | - Resource Owner (User) <br> - Client <br> - Authorization Server <br> - Resource Server |
| **Security**        | Signed assertions ensure integrity and authenticity.         | Tokens are usually signed (JWT), sometimes encrypted.                                    |
| **Standard Used**   | XML (complex but powerful).                                  | JSON (simpler, modern).                                                                  |
| **Adoption**        | Older; enterprise-focused (SAML 2.0).                        | Modern; widely used in APIs and mobile apps.                                             |

---

### **Flow Comparison**

#### **1. SAML Flow (Single Sign-On Authentication):**
- **Purpose**: Authenticate a user to access multiple applications.  
- **Participants**: Identity Provider (IdP) and Service Provider (SP).  
- **Steps**:  
   1. User tries to access a Service Provider (e.g., a corporate app).  
   2. SP redirects the user to the Identity Provider for authentication.  
   3. IdP verifies credentials and sends a **signed SAML Assertion** (XML document) back to the SP.  
   4. SP validates the assertion and grants access.  

**Example Use Case**: Logging into your corporate email, CRM, and HR systems using the same credentials.

---

#### **2. OAuth Flow (Authorization):**
- **Purpose**: Grant an application permission to access user resources (APIs, data).  
- **Participants**:  
   - **Resource Owner** (User): Owns the data/resource.  
   - **Client**: The application requesting access.  
   - **Authorization Server**: Issues tokens.  
   - **Resource Server**: Hosts the protected resources.  

- **Steps (OAuth 2.0 Authorization Code Flow):**  
   1. User consents to allow a Client (e.g., a third-party app) to access their resources.  
   2. Client redirects the user to the **Authorization Server** for permission.  
   3. Authorization Server issues an **Access Token**.  
   4. Client uses the token to access the **Resource Server**.  

**Example Use Case**: Allowing a fitness app to read your Google Calendar (via Google OAuth).

---

### **Key Similarities**

- Both are **standards** used for secure communication and access control.  
- Both can handle **authentication** flows (though OAuth is mainly for authorization).  
- Both ensure security through **token-based mechanisms** (SAML Assertion for SAML and JWT for OAuth).  
- Both involve **redirecting users** for authentication/authorization approval.

---

### **When to Use SAML vs. OAuth**

| **Scenario**                            | **Use SAML**                             | **Use OAuth**                                             |
| --------------------------------------- | ---------------------------------------- | --------------------------------------------------------- |
| **Enterprise SSO**                      | For internal apps (e.g., Okta, ADFS).    | Not ideal for SSO (OAuth can use OpenID Connect instead). |
| **Accessing APIs**                      | Not suited for API access.               | Ideal for APIs, mobile apps, and external integrations.   |
| **Legacy Applications**                 | SAML integrates well with older systems. | OAuth is more modern and flexible.                        |
| **Delegating Resource Access**          | Not designed for delegation.             | OAuth excels at delegation (e.g., access Google Drive).   |
| **Lightweight Web/Mobile Applications** | Too heavy due to XML processing.         | Lightweight; uses JSON tokens.                            |

---

### **Extending OAuth for Authentication: OpenID Connect (OIDC)**

OAuth 2.0 alone **does not handle authentication**. However, an extension called **OpenID Connect (OIDC)** adds authentication capabilities on top of OAuth.  

**How OIDC Fits In:**
- OIDC provides **identity tokens** to verify a user’s identity.  
- OIDC works similarly to SAML for authentication but uses **JSON Web Tokens (JWT)** instead of XML.  
XML vs JWT web tokens

**Example Use Case**: Signing into an app using "Log in with Google" (OIDC over OAuth 2.0).

---

### **Conclusion**

- **SAML** is a mature, XML-based protocol mainly used for **Single Sign-On (SSO)** in enterprise environments.  
- **OAuth** is a modern, lightweight standard for **authorization**, allowing applications to access resources without sharing user credentials.  

If you need **authentication and SSO**: Use **SAML** or **OpenID Connect**.  
If you need **authorization** for APIs or third-party access: Use **OAuth 2.0**.  
