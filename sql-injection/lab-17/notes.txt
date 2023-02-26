Lab #17 - SQL injection with filter bypass via XML encoding


End Goal: Exploit SQL injection to retrieve the admin user's credentials from the users table and log into their account.

Analysis:

1 UNION SELECT username || '~'  || password  FROM users