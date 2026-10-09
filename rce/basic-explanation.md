# RCE

Remote Code Execution (RCE) in Web Applications is a critical security
vulnerability that allows attackers to execute arbitrary code on the server
hosting the web application. This type of vulnerability arises when web
applications fail to properly validate and sanitize user input, allowing
attackers to inject and execute malicious code remotely. RCE vulnerabilities
are often the result of poor input validation, insecure coding practices, or
improper handling of user-controlled data.

Here's an example of vulnerable code in a PHP web application that demonstrates a simple RCE vulnerability:

```php
<?php
  // Vulnerable code that dynamically includes a file based on user input
  $page = $_GET['page']; // User-controlled input

  // Vulnerable include statement
  include($page . '.php');
?>
```

In the above code snippet, the value of the `page` parameter is directly
concatenated with the '.php' extension and passed to the `include()` function.
This can be exploited by an attacker by providing a malicious value for the
`page` parameter, such as:

```
http://example.com/vulnerable.php?page=malicious
```

If the application doesn't properly validate or sanitize the `page` parameter,
an attacker could inject arbitrary PHP code into the server, leading to RCE.
For example, an attacker could provide a payload like:

```
http://example.com/vulnerable.php?page=malicious.php%00
```

The `%00` is a null byte, which can bypass the file extension check and cause
PHP to interpret the file as `malicious.php` instead of `malicious.php`. This
allows the attacker to execute arbitrary PHP code contained within the
`malicious.php` file.

To prevent RCE vulnerabilities, web developers should avoid dynamically
including files based on user input and implement strict input validation and
sanitization mechanisms. Additionally, it's crucial to keep web application
frameworks and libraries up-to-date to mitigate known vulnerabilities.
