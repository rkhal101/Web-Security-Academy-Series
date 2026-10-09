# LFI vs Path Traversal

Local File Inclusion (LFI) and Path Traversal are two common web application vulnerabilities that involve accessing files on the server. While they have similarities, their goals and exploitation methods differ:

---

### **1. Local File Inclusion (LFI)**
- **Definition**: LFI occurs when a web application allows an attacker to include files from the server's filesystem, typically due to unsanitized user input in file path variables.
- **Objective**: The attacker aims to execute or view files on the server, often to gain sensitive information or escalate privileges.
- **Typical Target Files**:
  - `/etc/passwd`: To enumerate user accounts.
  - Web application configuration files containing database credentials.
  - Log files or other scripts that may contain sensitive data.

#### **Example**
- A vulnerable PHP script:
  ```php
  <?php include($_GET['file']); ?>
  ```
- Exploitation:
  ```
  http://example.com/vuln.php?file=../../etc/passwd
  ```
- **Result**: The `/etc/passwd` file's content is included and displayed.

#### **Potential Consequences**:
- Exfiltration of sensitive files.
- Execution of malicious code if the attacker can upload files and include them.
- Path Traversal may also be exploited during an LFI attack to access files outside the expected directory.

---

### **2. Path Traversal**
- **Definition**: Path Traversal (also called Directory Traversal) occurs when a web application improperly validates user-supplied file paths, allowing attackers to navigate to directories outside the intended scope.
- **Objective**: The attacker aims to **read files** outside the application's intended directory but usually cannot execute them directly (unlike LFI).
- **Typical Target Files**:
  - Files containing sensitive information, such as `/etc/passwd`, `/etc/hosts`, or application logs.
  - Configuration files like `web.config` (Windows) or `.env` (Linux).

#### **Example**
- A vulnerable PHP script:
  ```php
  <?php
  $file = $_GET['file'];
  include("uploads/" . $file);
  ?>
  ```
- Exploitation:
  ```
  http://example.com/vuln.php?file=../../../../etc/passwd
  ```
- **Result**: The attacker gains access to the `/etc/passwd` file.

#### **Potential Consequences**:
- Disclosure of sensitive system files.
- Exposure of application secrets and configurations.

---

### **Key Differences Between LFI and Path Traversal**

| **Aspect**               | **Local File Inclusion (LFI)**                                   | **Path Traversal**                                            |
| ------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------- |
| **Primary Goal**         | Include and possibly execute files on the server.                | Read files outside intended directories.                      |
| **Scope**                | Targets files for inclusion, often leading to code execution.    | Primarily targets reading file contents.                      |
| **Code Execution**       | Possible if the attacker can include files with executable code. | Not possible directly (unless combined with another exploit). |
| **Typical Exploitation** | Exploits `include()` or `require()` functions.                   | Exploits improper path validation.                            |
| **Examples**             | Include PHP scripts, configuration files, or logs.               | Access `/etc/passwd`, `.env`, or logs.                        |

---

### **Prevention for Both**
1. **Sanitize and Validate User Inputs**:
   - Use a whitelist approach for allowed file paths or names.
   - Reject inputs containing special characters like `..`, `/`, or `\`.

2. **Use Full File Paths**:
   - Resolve file paths to canonical paths and check them against an allowed directory.

3. **Restrict Permissions**:
   - Limit file permissions and access to sensitive directories.
   - Ensure web servers run with minimal privileges.

4. **Disable Unnecessary Functions**:
   - Disable dangerous PHP functions like `include`, `require`, or `exec` if not needed.

5. **Employ Web Application Firewalls (WAFs)**:
   - WAFs can block malicious payloads attempting to exploit LFI or Path Traversal vulnerabilities.

---

### **Summary**
- **LFI** is about including files, often leading to code execution.
- **Path Traversal** is about navigating to unauthorized directories to read files.
Both vulnerabilities stem from improper handling of file paths and inputs, and the best defenses are strong input validation and proper file access controls.
