#!/usr/bin/env python3

"""
main.py

SYNOPSIS
========
::

GET & POST requests.
Just playing around with this one.
Makes a request to a user supplied URL, uses the try-except block to handle errors,
and the conditional if-elif-else block to check the status of the request.
The response is printed to the screen.

"""
import argparse
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
from samba.dcerpc.dcerpc import payload

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


class Request:
    """
    This class uses the POST and GET, methods to make http requests to a user supplied URL.
    """
    def __init__(self, url, method=''):
        self.url = url
        self.method = method

    def get_request(self):
        """Make a GET request to a user supplied URL."""
        try:
            response = requests.get(self.url, verify=False, proxies=proxies)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.prettify())
        except requests.exceptions.RequestException as e:
            print(e)

    def post_request(self):
        """Make a POST request to a user supplied URL."""
        try:
            response = requests.post(self.url, verify=False, proxies=proxies, data=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.prettify())
        except requests.exceptions.RequestException as e:
            print(e)

    # The payload will be appended to the end of URL.
    @staticmethod
    def exploit(url, payload):
        """Exploit function that accepts a URL and a payload as arguments."""
        try:
            response = requests.post(url, verify=False, proxies=proxies, data=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.prettify())
        except requests.exceptions.RequestException as e:
            print(e)


# main function
def main(name):
    """Main function. Parses the command line arguments and executes the appropriate function."""
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', required=True, help='URL to be exploited')
        parser.add_argument('-p', '--payload', required=True, help='Payload to be appended to the URL')
        parser.add_argument('-m', '--method', required=True, help='Method to be used for the request')
        args = parser.parse_args()
        url = args.url
        payload = args.payload
        method = args.method
        Request(url, method).exploit(url, payload)
        Request(url, method).get_request()
        Request(url, method).post_request()
        Request(url, method).exploit(url, payload)
        Request(url, method).get_request()
    except IndexError:
        print(f'Usage: {name} -u <url> -p <payload> -m <method>')
        sys.exit(1)


# guarding the name variable
if __name__ == '__main__':
    main(sys.argv)
