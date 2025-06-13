## Here will be a collection of various GoBuster commands to make it easier and faster

**Attacking Directories**
```bash
# Template
gobuster dir --url http://{target_IP}/ --wordlist {wordlist_location}/directory-list-2.3-small.txt
```
<br>

```bash
# Example
gobuster dir --url  http://10.129.248.189 --wordlist  /opt/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
```
<br>
