## Blind XXE with out-of-band interaction


This lab has a "Check stock" feature that parses XML input but does not display the result.
You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.
To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

### Select a product from the home page, then click the check stock button
![Screenshot_20240611_182347](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/c396bc87-3468-4306-a948-1c9a5fd7134b)

### Check the HTTP history under the proxy tab
**and send the post stock check request:**

![xxe-post-stock-check-req](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/cd753e47-fdb0-4efa-b407-54f0c2d15976)

```http
POST /product/stock HTTP/1.1
```
**to the repeater**

You must follow the same logic as in the previous labs, and since the goal is to trigger an out-of-band interaction,
you're gonna have to refrence a declared external entity to a url you control: this would be the Burp Collaborator.
So go and copy the collaborator url/payload to clipboard and place it in the same location as in the classic
/etc/passwd attack.

Declare the doctype and assign it a name, I named mine foo, (though what you name it doesn't matter). Then paste the collaborator payload after the ENTITY SYSTEM call,(I named it bar,
but the name doesn't matter, so long as you reference it in the correct XML tags, prefix it with an ampersand `&` and suffix with a semicolon.
![Screenshot_20240611_182248](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/c2ba80ab-f452-4e4d-8b94-e7acbefc73f9)

![xxe-oob-collab-req](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/4a712295-69f7-4439-9160-e86fb286cb07)

then send the request. the response will say "Invalid product ID". Ignore that, and go check the Collaborator
for the out-of-band interaction.
![xxe-oob-collab-dns-lookup](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/e6607d78-5990-4fb3-8673-cc9bc0673c15)

The lab is now solved.


