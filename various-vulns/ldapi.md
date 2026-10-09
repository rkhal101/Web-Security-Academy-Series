### **What is LDAP Injection?**

**LDAP Injection** is a vulnerability that occurs when user-controlled input is incorporated into a Lightweight Directory Access Protocol (LDAP) query without proper validation or sanitization. This allows attackers to modify the structure of the LDAP query, potentially gaining unauthorized access to sensitive information or performing unauthorized actions.

---

### **How Does LDAP Injection Work?**

LDAP is used to access and manage directory services, such as authentication systems or organizational data (e.g., Active Directory). Vulnerable applications may directly use user input in LDAP filters without sanitizing it, enabling attackers to inject malicious LDAP syntax.

#### **Example of a Vulnerable LDAP Query:**

```java
String ldapQuery = "(&(uid=" + userInput + ")(password=" + passwordInput + "))";
```

- If an attacker inputs the following for `userInput`:
    
    ```plaintext
    *))(|(uid=*
    ```
    
- The resulting query becomes:
    
    ```plaintext
    (&(uid=*))(|(uid=*))(password=attack)
    ```
    
- This query can bypass authentication by matching any user (`uid=*`).

---

### **Vulnerabilities of LDAP Injection**

LDAP injection vulnerabilities arise from:

1. **Improper Input Handling:**
    - User input is concatenated into LDAP queries without sanitization.
2. **Lack of Input Validation:**
    - Applications do not validate or restrict the format of user input.

#### **Consequences of LDAP Injection:**

1. **Authentication Bypass:**
    - Attackers can manipulate queries to bypass authentication checks.
2. **Information Disclosure:**
    - Sensitive information such as user credentials or organizational details may be exposed.
3. **Privilege Escalation:**
    - Attackers may exploit LDAP injection to modify user roles or access permissions.
4. **Denial of Service (DoS):**
    - Crafted queries can overwhelm the directory service, disrupting normal operations.

---

### **Exploiting LDAP Injection**

#### **Common Exploitation Scenarios:**

1. **Authentication Bypass:**
    
    - Attacker Input for `userInput`:
        
        ```plaintext
        *))(|(uid=*
        ```
        
    - Resulting Query:
        
        ```plaintext
        (&(uid=*))(|(uid=*))(password=attack)
        ```
        
    - This query always evaluates to true, allowing the attacker to bypass authentication.
2. **Information Disclosure:**
    
    - Attacker Input for `userInput`:
        
        ```plaintext
        *))(|(objectClass=*)
        ```
        
    - Resulting Query:
        
        ```plaintext
        (&(uid=*))(|(objectClass=*))(password=attack)
        ```
        
    - This can enumerate all objects within the directory.
3. **Privilege Escalation:**
    
    - Attacker Input:
        
        ```plaintext
        admin)(role=admin
        ```
        
    - Resulting Query:
        
        ```plaintext
        (&(uid=admin)(role=admin)(password=attack))
        ```
        
    - This could escalate the attacker’s privileges if roles are managed via LDAP.
4. **Denial of Service:**
    
    - Recursive or overly broad queries can consume server resources and cause DoS.

---

### **Preventing LDAP Injection**

#### **1. Use Parameterized Queries:**

- Many modern LDAP libraries support parameterized queries, which separate query logic from input values.

#### **2. Sanitize and Escape User Input:**

- Properly escape special LDAP characters such as `*`, `(`, `)`, `\`, and `|`.
- Example (Java):
    
    ```java
    String sanitizedInput = StringEscapeUtils.escapeLDAP(userInput);
    ```
    

#### **3. Validate Input:**

- Implement strict validation to ensure user input matches expected formats (e.g., alphanumeric usernames).

#### **4. Limit Query Scope:**

- Restrict LDAP queries to the minimum required scope, limiting the potential for abuse.

#### **5. Use Authentication Mechanisms:**

- Authenticate users against stored credentials instead of relying solely on LDAP queries.

#### **6. Monitor and Log Queries:**

- Track unusual patterns in LDAP queries to detect potential injection attempts.

---

### **Detecting and Exploiting LDAP Injection in Penetration Testing**

#### **Steps for Testing:**

1. **Identify Inputs:**
    
    - Look for user-controlled inputs that influence LDAP queries, such as login forms or search functionality.
2. **Inject LDAP Special Characters:**
    
    - Test whether the application accepts special characters like `*`, `(`, `)`, `|`, and `\`.
    - Example Payload:
        
        ```plaintext
        *))(|(uid=*
        ```
        
3. **Enumerate Objects:**
    
    - Use crafted queries to extract data from the directory.
    - Example:
        
        ```plaintext
        *))(|(objectClass=*)
        ```
        
4. **Test Authentication Bypass:**
    
    - Inject payloads to bypass login checks.
    - Example Payload:
        
        ```plaintext
        admin*))(|(uid=*
        ```
        
5. **Privilege Escalation Testing:**
    
    - Attempt to modify roles or access levels using injection payloads.

#### **Tools for LDAP Injection Testing:**

- **Burp Suite:** Intercept and modify requests with LDAP payloads.
- **OWASP ZAP:** Automate testing for injection vulnerabilities.
- **Custom Scripts:** Use custom scripts to craft and send LDAP queries.

---

### **Example Exploitation Scenario**

#### Vulnerable Query:

```java
String ldapQuery = "(&(uid=" + userInput + ")(password=" + passwordInput + "))";
```

#### Malicious Input:

- `userInput`: `*))(|(uid=*))`
- `passwordInput`: `anything`

#### Resulting Query:

```plaintext
(&(uid=*))(|(uid=*))(password=anything)
```

#### Outcome:

- Authentication bypass: The query evaluates to true for all users.

---

### **Conclusion**

LDAP injection is a severe security risk that can lead to authentication bypass, information disclosure, privilege escalation, and more. To mitigate these risks, applications must use parameterized queries, sanitize input, and validate user data rigorously. Penetration testers should focus on identifying vulnerable LDAP queries and exploit paths to assess the application's resilience to this class of attack.
