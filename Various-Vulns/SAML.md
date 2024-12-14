# **What is Security Assertion Markup Language (SAML)?**

SAML (Security Assertion Markup Language) is an open standard for exchanging authentication and authorization data between parties, specifically:

1. **Identity Provider (IdP):** The entity that authenticates users and provides identity information (e.g., Okta, Microsoft Azure AD).
2. **Service Provider (SP):** The application or service a user wants to access (e.g., a web app like Salesforce or Slack).

SAML enables **Single Sign-On (SSO)** functionality by allowing users to authenticate once with the IdP and gain access to multiple SPs without needing to log in again.

#### **Key Components:**

1. **Assertions:** XML-based statements about the user’s identity and attributes.
    - **Authentication Assertions:** Verify user identity.
    - **Attribute Assertions:** Provide additional user attributes.
    - **Authorization Assertions:** Define user permissions.
2. **Bindings:** How SAML messages are sent (e.g., HTTP POST, HTTP Redirect).
3. **Profiles:** Define specific SAML use cases like Web Browser SSO.

---

### **When and How is SAML Used?**

#### **Common Use Cases:**

1. **Single Sign-On (SSO):** Simplifies user authentication across multiple applications.
2. **Federated Identity Management:** Allows organizations to share user credentials securely between trusted partners.
3. **Cloud and SaaS Applications:** Used to integrate enterprise identity systems with external applications like Office 365, AWS, or Google Workspace.

#### **How it Works (Simplified SAML Workflow):**

1. **User Attempts Access:** A user tries to access an SP (e.g., Salesforce).
2. **Redirect to IdP:** The SP redirects the user to the IdP for authentication.
3. **Authentication at IdP:** The user logs in (or uses an existing session).
4. **SAML Assertion Generation:** The IdP creates a SAML assertion containing authentication and user details.
5. **Assertion Validation by SP:** The SP validates the assertion and grants or denies access.

---

### **SAML Security Vulnerabilities**

Although SAML is widely used, it can be vulnerable if not implemented or configured correctly.

#### **Common Vulnerabilities:**

1. **XML Signature Wrapping (XSW):**
    
    - An attacker modifies the SAML message by injecting malicious elements while keeping the digital signature valid.
    - Exploited if the SP doesn’t properly validate the signed parts of the message.
2. **Replay Attacks:**
    
    - An attacker intercepts a valid SAML assertion and reuses it to gain unauthorized access.
    - Mitigation: Assertions should have timestamps and be marked as one-time use.
3. **Improper Validation of Assertions:**
    
    - The SP fails to verify the digital signature or assumes an assertion is valid without checking it.
4. **Man-in-the-Middle (MitM) Attacks:**
    
    - If communication between the IdP and SP isn’t encrypted (e.g., no HTTPS), attackers can intercept and manipulate SAML data.
5. **Misconfigured Metadata:**
    
    - If the IdP or SP metadata is improperly configured, attackers can exploit trust relationships.
6. **Disclosure of Sensitive Data:**
    
    - Assertions may carry sensitive user data (e.g., email, roles) that could be exposed if intercepted.

---

### **Relevance to Web Application Penetration Testing**

SAML is an important area of focus in penetration testing, especially for applications using SSO or federated authentication.

#### **Why Test SAML?**

- Exploiting vulnerabilities in SAML can lead to privilege escalation, unauthorized access, or data breaches.
- SAML is a critical part of authentication workflows, and weaknesses here can undermine the entire security posture of the web app.

#### **Penetration Testing Techniques:**

1. **Test for XML Signature Wrapping:**
    - Modify the signed SAML message to include additional unauthorized attributes and check if they are accepted.
2. **Replay Attacks:**
    - Attempt to reuse intercepted SAML assertions.
    - Verify the presence of nonce or timestamp mechanisms.
3. **Inspect Configuration:**
    - Check if assertions are encrypted and signatures are validated properly.
    - Ensure strong certificate validation between IdP and SP.
4. **Check for Misconfigured Metadata:**
    - Analyze trust relationships and ensure strict validation of certificates and endpoints.
5. **Session Hijacking:**
    - Intercept and analyze SAML tokens in transit using tools like Burp Suite or Wireshark.
    - Look for unencrypted assertions or insecure communications.

#### **Tools for SAML Testing:**

- **Burp Suite**: For intercepting and modifying SAML requests/responses.
- **SAML Raider**: A Burp extension for SAML testing.
- **Wireshark**: To capture and analyze SAML traffic.
- **Custom Scripts**: To replay, manipulate, or fuzz SAML assertions.

---

### **Conclusion**

SAML plays a critical role in authentication and authorization for web applications. Its vulnerabilities can have severe consequences if exploited. Understanding how SAML works and its potential weaknesses is essential for penetration testing and securing web applications that rely on federated identity management.

CORS Vulnerabilities

CORS (Cross-Origin Resource Sharing) is a security feature that enables web pages to make requests to a different origin (domain, protocol, or port) than the one the web page was loaded from. However, misconfigurations in CORS can lead to vulnerabilities, allowing attackers to steal sensitive data, perform XSS attacks, or execute remote code. Here are some common CORS web app vulnerabilities:

1. **Reflected Origins**: When an application sets `Access-Control-Allow-Origin` to an attacker-supplied domain and allows credentials (`Access-Control-Allow-Credentials: true`), an attacker can inject a malicious script and steal sensitive data.

Exploitation: Host a JS script on an external server, create an HTML page with the script, and send it to the user. The script will make a CORS request to the vulnerable application, allowing the attacker to retrieve sensitive data.

2. **Null Origins**: When an application sets `Access-Control-Allow-Origin` to `null` and allows credentials (`Access-Control-Allow-Credentials: true`), an attacker can set the `Origin` header to `null` and retrieve sensitive data.

Exploitation: Host a JS script on an external server, add an iframe sandbox to set the frame's origin to `null`, and make a CORS request to the vulnerable application.

3. **Trusted Subdomains**: When an application sets `Access-Control-Allow-Origin` to any of its subdomains and allows credentials (`Access-Control-Allow-Credentials: true`), an attacker can exploit an XSS vulnerability in the subdomain to steal sensitive data or perform unauthorized actions.

Exploitation: Check if the subdomain has an XSS vulnerability and inject a malicious script. The script will make a CORS request to the vulnerable application, allowing the attacker to steal sensitive data.

4. **Wildcard Origins**: Although not exploitable in itself, a wildcard (`*`) in `Access-Control-Allow-Origin` can be a sign of poor CORS implementation. If the application also sets `Access-Control-Allow-Credentials: true`, it may be vulnerable to other attacks.

**Mitigations**

1. Implement proper CORS headers: Set `Access-Control-Allow-Origin` to only trusted domains and restrict access to sensitive data.
2. Restrict access to sensitive data: Use authentication and authorization mechanisms to control access to sensitive data.
3. Use secure protocols: Ensure that all requests and responses use HTTPS (TLS) to prevent man-in-the-middle attacks.
4. Validate user input: Sanitize and validate user input to prevent XSS attacks.

**Detection and Testing**

1. Use Burp Suite or Chrome DevTools to search for CORS headers in responses.
2. Test for CORS misconfigurations by setting the `Origin` header to different values (e.g., attacker-supplied domain, null, or subdomain).
3. Verify that the application responds correctly to each test case.

**Conclusion**

CORS web app vulnerabilities can have severe consequences, including data theft and unauthorized access. By understanding these vulnerabilities and implementing proper CORS configurations, you can protect your web application from these threats. Remember to validate user input, use secure protocols, and restrict access to sensitive data to ensure the security of your application.
