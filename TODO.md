# TODO: Repository Naming Convention Cleanup

Tracking file for normalizing directory and file names across the repo.
**STATUS: COMPLETE.** All renames below were executed with `git mv` and committed:

- `refactor: rename directories to lowercase-kebab-case` (16 dirs)
- `refactor: rename files to naming convention (md kebab-case, py snake_case)` (17 `.md` + 76 `.py`)
- Link check (README.md, main.py, scripts/, cross-note markdown links): no stale
  references found, so no link-fix commit was needed.

## Convention

- **Directories:** `lowercase-kebab-case` (all lowercase, words joined by hyphens).
- **`.md` files:** `lowercase-kebab-case`.
- **`.py` files:** `snake_case` (decided — per `AGENTS.md`).

Rationale for kebab-case directories:

- Already the majority style (17 of 33 directories conform), so the minority is converted.
- Hyphens over underscores: web/Git convention, no shift key, not swallowed by underlined-link rendering.
- All-lowercase avoids case-sensitivity bugs between case-insensitive (macOS/Windows) and case-sensitive (Linux) filesystems.
- Acronyms stay readable lowercased (`jwt`, `saml`, `ssti`) and match existing initialisms (`cors`, `csrf`, `ssrf`, `xss`).

---

## 1. Directory renames (16)

Approved convention; **not yet executed.**

| Current name | New name |
|---|---|
| `API` | `api` |
| `CI-CD-Security-Testing` | `ci-cd-security-testing` |
| `Checklist` | `checklist` |
| `DeleteCarlos` | `delete-carlos` |
| `Extra` | `extra` |
| `GraphQL-API` | `graphql-api` |
| `HTTP_Request_Smuggling` | `http-request-smuggling` |
| `Insecure-Deserialization` | `insecure-deserialization` |
| `JWT` | `jwt` |
| `LFI` | `lfi` |
| `LLM` | `llm` |
| `RCE` | `rce` |
| `SAML` | `saml` |
| `SSTI` | `ssti` |
| `Various-Vulns` | `various-vulns` |
| `turbo_intruder_scripts` | `turbo-intruder-scripts` |

Already conforming (17, no change): `broken-access-control`, `broken-authentication`,
`business-logic-vulnerabilities`, `clickjacking`, `command-injection`, `cors`, `csrf`,
`directory-traversal`, `dom-based-vulnerabilities`, `file-upload-vulnerabilities`,
`information-disclosure`, `scripts`, `sql-injection`, `ssrf`, `websockets-vulnerabilities`,
`xss`, `xxe-injection`.

**Caveat — case-only renames** (`API`→`api`, `JWT`→`jwt`, `LFI`→`lfi`, `LLM`→`llm`,
`RCE`→`rce`, `SAML`→`saml`, `SSTI`→`ssti`): on case-insensitive filesystems a direct
`git mv API api` can fail or no-op. Use a two-step: `git mv API tmp && git mv tmp api`.

---

## 2. Reference check (done — no breakage)

Grepped `README.md`, `main.py`, and `scripts/` for the 16 old directory names.
(No `.github/` directory exists.)

| file:line | Line content | Real path ref? |
|---|---|---|
| `README.md:39` | `[**Hack Tricks API Pentesting**](https://book.hacktricks.xyz/...)` | No — prose/URL |
| `README.md:40` | `[**API Key Hacks: ... API keys discoverd on Bug Bounties**](...)` | No — prose |
| `README.md:45` | `[**OWASP Top Ten 2023 - API**](https://owasp.org/API-Security/...)` | No — prose/URL |

All three are the word "API" in a links section, not references to the `API/`
directory. **No path references to any renamed directory exist** in those files — the
directory renames break nothing there.

---

## 3. `.md` file renames (17)

`.md` files whose basename is not lowercase-kebab-case. Parent directories shown as
current; they change under section 1.

| Current path | Proposed basename |
|---|---|
| `API/API_Vulnerabilities.md` | `api-vulnerabilities.md` |
| `API/crAPI-NotesAndChallenges.md` | `crapi-notes-and-challenges.md` |
| `Checklist/WebAppPentest_Checklist_Enhanced.md` | `webapp-pentest-checklist-enhanced.md` |
| `Extra/Checklist.md` | `checklist.md` |
| `Extra/ExtraBurpSuiteStuff.md` | `extra-burpsuite-stuff.md` |
| `Extra/WebAppHackers_Checklist.md` | `webapp-hackers-checklist.md` |
| `GraphQL-API/General_Info.md` | `general-info.md` |
| `RCE/Basic_Explination.md` | `basic-explanation.md` ⚠️ typo: "Explination" |
| `SSTI/SSTI.md` | `ssti.md` |
| `Various-Vulns/LDAPi.md` | `ldapi.md` |
| `Various-Vulns/SAML.md` | `saml.md` |
| `sql-injection/lab-01/ExploitScriptInfo.md` | `exploit-script-info.md` |
| `sql-injection/lab-02/script_info.md` | `script-info.md` |
| `sql-injection/lab-16/Blind_SQLi_with_OutOfBandDataExfiltration.md` | `blind-sqli-with-out-of-band-data-exfiltration.md` |
| `xss/Notes/DOM-Based-Vulns.md` | `dom-based-vulns.md` |
| `xss/Notes/XSS-Contexts.md` | `xss-contexts.md` |
| `xxe-injection/lab-03/lab_03.md` | `lab-03.md` |

**`README.md` — keep as-is.** Flagged by the uppercase check, but it's a universal
convention that GitHub/GitLab render specially; lowercasing would be a regression.

---

## 4. `.py` file renames — snake_case (decided: option B)

Per `AGENTS.md`, `.py` files use `snake_case`. This supersedes the repo's current
dominant kebab-case `.py` style, so **~80 files** rename: every hyphen becomes an
underscore, plus the handful with uppercase/camelCase/typos. The full list comes from
`git ls-files '*.py'`; the rule is mechanical (`s/-/_/g`, lowercase, fix the 6 oddballs
below), so it will be generated and shown as a plan before any `git mv` runs.

The **6 true outliers** need more than a hyphen swap:

| Current path | Issue | → snake |
|---|---|---|
| `HTTP_Request_Smuggling/CL-TE.py` | uppercase | `cl_te.py` |
| `HTTP_Request_Smuggling/H2-TE.py` | uppercase | `h2_te.py` |
| `HTTP_Request_Smuggling/H2-Tunnel.py` | uppercase | `h2_tunnel.py` |
| `HTTP_Request_Smuggling/TE-CL.py` | uppercase | `te_cl.py` |
| `turbo_intruder_scripts/specialWordlists.py` | camelCase | `special_wordlists.py` |
| `file-upload-vulnerabilities/lab-04/file-uplod-lab-04.py` | typo "uplod" | `file_upload_lab_04.py` |

All other `.py` files are clean kebab-case (`access-control-lab-01.py`, `sqli-lab-01.py`,
`ssrf-lab-05.py`, …) and convert by the mechanical rule alone (e.g.
`access-control-lab-01.py` → `access_control_lab_01.py`).

> Note: this is a near-total rename of the `.py` corpus. Per the working rule in
> `AGENTS.md`, the full plan will be shown and approved before editing more than 5 files.

---

## Notes / loose ends

- Two proposals fix embedded typos (`Explination`→`explanation`; `file-uplod`→`file-upload`).
  Flag if the misspelling should be preserved in the filename instead.
- Nested subfolders are also mixed-case (`xss/Notes`, `xss/Exploits` vs `*/theory`);
  not `.md`/`.py` files, so outside this audit. Flag to fold them in.
- Renames should use `git mv` to preserve history.
- After renames: re-check `README.md` and cross-note links for any now-stale paths.
