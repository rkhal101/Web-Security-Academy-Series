#!/usr/bin/env python3
"""
Simple HTTP request tool with GET/POST support and proxy + SSL bypass.
You will find stand-alone scripts like this in each of the lab topic folders.
Useful boiler plate code for making basic exploits for the labs.
Or, use this as the entry point for something else...
"""

import argparse
import sys
import urllib3
import requests
from bs4 import BeautifulSoup

# Take care of proxy stuff to run requests throug Burp
# Disable SSL verification warnings (only if you're intentionally bypassing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration for BurpSuite
PROXIES = {
    'http':  'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}


class HttpRequester:
    """
    Simple class to make GET or POST requests to a given URL,
    with optional proxy support and SSL verification disabled.
    """
    def __init__(self, url: str, method: str = "GET"):
        self.url = url.strip()
        self.method = method.upper()
        if self.method not in ("GET", "POST"):
            raise ValueError(f"Unsupported HTTP method: {method}. Use GET or POST.")

    def make_request(self, data: dict | str | None = None) -> None:
        """
        Execute the HTTP request based on the method set during initialization.
        Prints the prettified HTML response if successful.
        """
        try:
            if self.method == "GET":
                response = requests.get(
                    self.url,
                    verify=False,
                    proxies=PROXIES,
                    timeout=15
                )
            else:  # POST
                response = requests.post(
                    self.url,
                    verify=False,
                    proxies=PROXIES,
                    data=data,           # can be dict (form) or str (raw)
                    timeout=15
                )

            response.raise_for_status()  # raise exception for 4 and 500s

            # Parse and pretty-print HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"\n=== {self.method} Response from {self.url} ===\n")
            print(soup.prettify())
            print(f"\n=== Status: {response.status_code} ===\n")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple HTTP GET/POST requester with proxy support",
        epilog="Example:\n"
               "  python main.py -u http://example.com/login -m POST -p 'username=admin&password=test'",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-u', '--url', required=True,
                        help="Target URL")
    parser.add_argument('-m', '--method', required=True,
                        help="HTTP method (GET or POST)")
    parser.add_argument('-p', '--payload', default=None,
                        help="POST data (form-encoded string or key=value pairs)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # CREATE THE REQUESTER INSTANCE/OBJECT
        requester = HttpRequester(url=args.url, method=args.method)

        if requester.method == "POST" and args.payload:
            print(f"Sending POST payload: {args.payload}")
            requester.make_request(data=args.payload)
        else:
            requester.make_request()

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user.", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
