### **What is Cross-Origin Resource Sharing (CORS)?**

**Cross-Origin Resource Sharing (CORS)** is a web security feature that allows controlled access to resources (e.g., APIs, fonts, or data) on a web server from a different domain (origin). Browsers enforce a **Same-Origin Policy (SOP)** by default, restricting web pages from making requests to a different domain unless explicitly permitted via CORS.

---

### **How CORS Works**

When a browser makes a cross-origin request, it performs one of two types of requests:

1. **Simple Requests:**
    
    - Performed directly without a preflight check.
    - Allowed if certain conditions are met, such as using HTTP methods like `GET` or `POST` with safe headers.
2. **Preflight Requests:**
    
    - For more complex interactions, the browser sends an `OPTIONS` request to the server to check whether the actual request is allowed.
    - If the server responds with appropriate headers, the browser proceeds with the actual request.

#### **Key CORS Headers:**

- **Access-Control-Allow-Origin:** Specifies which origins are allowed (`*` allows all).
- **Access-Control-Allow-Methods:** Specifies HTTP methods allowed for cross-origin requests.
- **Access-Control-Allow-Headers:** Specifies which headers can be sent in the request.
- **Access-Control-Allow-Credentials:** Indicates whether the response can expose credentials (e.g., cookies).

---

### **CORS Vulnerabilities**

CORS can become a security risk if misconfigured, potentially allowing unauthorized access to sensitive resources or user data.

#### **Common Misconfigurations:**

1. **Overly Permissive `Access-Control-Allow-Origin`:**
    
    - Using `*` (wildcard) for `Access-Control-Allow-Origin` allows any domain to access the resource. This is dangerous if sensitive data is exposed.
    - Example:
        
        ```http
        Access-Control-Allow-Origin: *
        ```
        
    - Exploitation: An attacker can make a malicious website send requests to the vulnerable server and gain access to sensitive data in the response.
2. **Dynamic Origin Reflection:**
    
    - Some servers reflect the `Origin` header value without proper validation, trusting any origin.
    - Example:
        
        ```http
        Access-Control-Allow-Origin: https://<origin_from_request>
        ```
        
    - Exploitation: An attacker can set the `Origin` to their malicious domain and gain access to sensitive information.
3. **Improper Use of `Access-Control-Allow-Credentials`:**
    
    - Setting `Access-Control-Allow-Credentials: true` allows cookies and other credentials to be included in cross-origin requests.
    - Exploitation: Combined with permissive `Access-Control-Allow-Origin`, this enables unauthorized access to authenticated resources.
4. **Exposing Sensitive Methods:**
    
    - Allowing dangerous HTTP methods like `DELETE`, `PUT`, or `PATCH` through `Access-Control-Allow-Methods`.
5. **Misconfigured Preflight Responses:**
    
    - Preflight responses may incorrectly allow origins or methods that shouldn't be authorized.

---

### **Exploits Against CORS**

Here are some common exploits targeting CORS misconfigurations:

#### 1. **Unauthorized Data Access**

- **Scenario:** An API endpoint exposes user data with an overly permissive `Access-Control-Allow-Origin: *`.
- **Attack:** An attacker creates a malicious website that sends a cross-origin `GET` request to the vulnerable API. If the API returns sensitive data in the response, the attacker can steal it.

#### 2. **Session Hijacking with Credentials**

- **Scenario:** `Access-Control-Allow-Credentials: true` is used with a permissive or dynamically reflected `Access-Control-Allow-Origin`.
- **Attack:**
    - The attacker crafts a malicious site that sends a cross-origin request.
    - If the victim is logged into the target application, the browser includes their session cookies.
    - The attacker can read the authenticated response.

#### 3. **CSRF via CORS**

- **Scenario:** A web application accepts cross-origin `POST` requests but doesn't properly validate the origin.
- **Attack:** The attacker tricks the victim into visiting a malicious site that makes a `POST` request to the target application (e.g., changing account details).

#### 4. **Preflight Abuse**

- **Scenario:** A server responds incorrectly to `OPTIONS` requests, granting access to unsafe methods or headers.
- **Attack:** The attacker can exploit this misconfiguration to send unauthorized `DELETE` or `PUT` requests.

---

### **Defending Against CORS Exploitation**

To prevent exploitation, follow these best practices:

1. **Restrict Origins:**
    
    - Avoid using `*` for `Access-Control-Allow-Origin`.
    - Explicitly specify trusted origins.
    - Example:
        
        ```http
        Access-Control-Allow-Origin: https://trusted-origin.com
        ```
        
2. **Avoid Dynamic Reflection:**
    
    - Do not blindly reflect the `Origin` header. Validate against a whitelist of trusted domains.
3. **Be Careful with Credentials:**
    
    - Use `Access-Control-Allow-Credentials: true` only if absolutely necessary.
    - Pair it with a specific, trusted origin.
4. **Limit Allowed Methods and Headers:**
    
    - Only allow necessary HTTP methods and headers in `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers`.
5. **Secure Preflight Responses:**
    
    - Ensure `OPTIONS` requests only allow intended origins, methods, and headers.
6. **Use HTTPS:**
    
    - Always enforce HTTPS to prevent MitM attacks.

---

### **Relevance to Penetration Testing**

Testing CORS is crucial in identifying potential data leaks or unauthorized access points in web applications. Here’s how a pentester might approach it:

1. **Check CORS Headers:**
    
    - Analyze responses to see if `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, or other headers are misconfigured.
2. **Exploit Origin Reflection:**
    
    - Use tools like Burp Suite to craft requests with malicious `Origin` headers and observe if the server reflects them.
3. **Test with Credentials:**
    
    - Verify if `Access-Control-Allow-Credentials` exposes sensitive data when combined with permissive origins.
4. **Simulate CSRF via CORS:**
    
    - Attempt cross-origin requests to verify if unauthorized actions can be performed.
5. **Inspect API Responses:**
    
    - Check if sensitive information is exposed in responses to cross-origin requests.

By systematically testing and addressing these issues, organizations can significantly enhance the security of their web applications.
