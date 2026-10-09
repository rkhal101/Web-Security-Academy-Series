#!/usr/bin/env python3

def login_wiener():
    logindata = {
        'username' : 'wiener',
        'password' : 'peter'
    }
    resp = s.post(login_url, data=logindata)
