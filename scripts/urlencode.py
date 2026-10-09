#!/usr/bin/env python3

def urlencode(s):
    encoded = ''
    for char in s:
        if char.isalnum() or char in ['.', '~', '-', '_']:
            encoded += char
        else:
            encoded += '%' + char.encode('utf-8').hex().upper()
    return encoded

def main():
    input_string = input("Enter the string you want to URL encode: ")
    encoded_string = urlencode(input_string)
    print(encoded_string)

if __name__ == "__main__":
    main()
