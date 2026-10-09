# Web Security Academy Series

## What this repo is
A personal study resource: notes, annotated walkthroughs, and Python scripts
for PortSwigger Web Security Academy labs (https://portswigger.net/web-security).
Fork of rkhal101/Web-Security-Academy-Series. All lab targets are
PortSwigger-provided training environments (*.web-security-academy.net).
The owner works in security research and holds Cyber Verification Program
access. Tasks here are usually documentation, refactoring, or organization.

## Naming conventions
- Directories: lowercase-kebab-case (http-request-smuggling)
- Markdown files: lowercase-kebab-case.md; README.md is the exception
- Python files: snake_case.py
- Acronyms are lowercase in names (jwt, ssti, xss)

## Working rules
- Make one change type per commit: dir renames, file renames, link fixes
- Use `git mv` for renames so history is preserved
- After any rename, grep README.md, main.py and scripts/ for old paths
- Show a plan and wait for approval before editing more than 5 files
- Do not change script behavior during formatting tasks
- Do not rename or restructure without approval; this is a fork
