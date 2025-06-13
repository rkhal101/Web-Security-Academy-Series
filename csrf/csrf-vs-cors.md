### **Difference Between Cross-Origin Resource Sharing (CORS) and Cross-Site Request Forgery (CSRF)**

While both concepts are related to web application security, they serve entirely different purposes and are not interchangeable. Here's an explanation of each:

---

### **Cross-Origin Resource Sharing (CORS):**
1. **Definition:**
   - CORS is a browser security feature that regulates how resources on a web page can be requested from a different domain (origin). It ensures that a website on **Origin A** can only fetch resources from **Origin B** if Origin B explicitly allows it.

2. **Purpose:**
   - It prevents unauthorized sharing of resources between different origins.
   - Example: A website hosted at `example.com` shouldn't arbitrarily make requests to `bank.com` without permission.

3. **How It Works:**
   - A browser sends a preflight request (using the `OPTIONS` method) to check whether the server of the other origin permits the requested action.
   - The server responds with headers like `Access-Control-Allow-Origin`, specifying allowed origins and methods.

4. **Common Use Case:**
   - Fetching API data from a third-party server in a front-end web application.

5. **Vulnerabilities:**
   - Poorly configured CORS headers (e.g., setting `Access-Control-Allow-Origin: *`) can allow attackers to access sensitive resources via malicious origins.

---

### **Cross-Site Request Forgery (CSRF):**
1. **Definition:**
   - CSRF is an attack where a malicious website tricks a user's browser into making unauthorized requests to another website (where the user is already authenticated) without their consent.

2. **Purpose of the Attack:**
   - The goal is to perform actions on behalf of an authenticated user without their knowledge.
   - Example: Transferring money from a logged-in user's bank account using a forged request.

3. **How It Works:**
   - An attacker embeds a malicious link or form in their website.
   - When the victim (logged in to the target site) interacts with the attacker's page, their browser sends a request to the target site, using the victim's session cookies.

4. **Common Use Case (Attack Scenario):**
   - A victim is logged into `bank.com`. The attacker lures the victim to a malicious website, which silently sends a request to `bank.com` to transfer funds without the victim's intent.

5. **Mitigation:**
   - Use CSRF tokens: A random token included in forms or headers that attackers cannot predict.
   - Verify the `Referer` or `Origin` headers.

---

### **Key Differences Between CORS and CSRF:**

| Feature                | **CORS**                                    | **CSRF**                                      |
|------------------------|---------------------------------------------|----------------------------------------------|
| **Purpose**            | Controls resource sharing across origins.  | Prevents unauthorized actions on behalf of a user. |
| **Nature**             | Browser security policy feature.           | Exploit or attack vector.                    |
| **Who Configures?**    | Server developers via headers.             | Developers mitigate CSRF by using tokens.    |
| **Focus Area**         | Focuses on allowing or blocking requests.  | Focuses on preventing malicious requests.    |
| **Affected Party**     | Impacts cross-origin requests.             | Exploits the trust between a user and their session. |

---

### **Examples:**

#### **CORS Example:**
- A front-end app at `example.com` needs to fetch user data from an API hosted at `api.example.org`.
- If the API server does not allow requests from `example.com` via its `Access-Control-Allow-Origin` header, the browser will block the request.

#### **CSRF Example:**
- You are logged into your online banking account at `bank.com`.
- An attacker creates a form on their malicious site with an action that performs a money transfer to their account:
  ```html
  <form action="https://bank.com/transfer" method="POST">
      <input type="hidden" name="amount" value="1000">
      <input type="hidden" name="to_account" value="attacker_account">
  </form>
  <script>
      document.forms[0].submit();
  </script>
  ```
- When you visit the attacker's page, the browser sends this form request to `bank.com` using your session, completing the transfer.

---

### **Summary:**
- **CORS** ensures safe and authorized resource sharing between origins by validating server configurations.
- **CSRF** exploits the trust a web app has in a user's browser session, tricking it into performing unauthorized actions.
