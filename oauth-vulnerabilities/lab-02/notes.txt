Lab #2 - SSRF via OpenID dynamic client registration

Vulnerable parameter - OAuth service registration endpoint.

Goal - To access the admin credentials endpoint and steal the secret access key.

creds - wiener:peter

Analysis:

https://oauth-0a9600da04a45e2e809b1fae02b40051.oauth-server.net/.well-known/openid-configuration


https://oauth-0a9600da04a45e2e809b1fae02b40051.oauth-server.net/reg