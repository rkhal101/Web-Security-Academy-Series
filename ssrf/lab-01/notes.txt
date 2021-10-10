Lab #1 - Basic SSRF against the local server

Vulnerable feature - stock check functionality

Goal - change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

Analysis:

localhost - http://localhost/
admin interface - http://localhost/admin
delete carlos - http://localhost/admin/delete?username=carlos

python3 lab-01.py www.example.com