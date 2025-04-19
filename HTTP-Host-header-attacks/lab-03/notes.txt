Lab #3 – Web cache poisoning via ambiguous requests

Vulnerable parameter - Host header

Goal - Perform a web cache poisoning attack that alerts on the victim's cookie

Analysis:

User           Cache          Web Server
Attacker ----------------------> Homepage
         <----------------------
User 2 ----------> Cached Homepage
       <----------

Three steps to construct a web cache poisoning attack:
1. Identify and evaluate unkeyed inputs.
2. Elicit a harmful response from the backend server.
3. Get the response cached.


 <script type="text/javascript" src="<host>/resources/js/tracking.js"></script>