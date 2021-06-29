import requests

auth = {
    'username': 'carlos.neto',
    'password': 'augustoliks',
    'target': ''
}

session = requests.Session()
session.post(
    'https://127.0.0.1:8443/login',
    verify=False,
    data=auth
)
auth_cookie = {'inventory_api_auth': session.cookies['inventory_api_auth']}

res = requests.get(
    'https://127.0.0.1:8443/api/read/hosts',
    verify=False,
    cookies=auth_cookie
)

print(res.json())
