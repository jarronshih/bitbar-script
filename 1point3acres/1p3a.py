#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import requests
import re
from http.cookies import SimpleCookie
from datetime import date

from local_settings import username, raw_cookies


def login_with_cookies(username, raw_cookies):
    # Utils
    main_url = 'https://www.1point3acres.com/bbs/'
    session_requests = requests.session()

    # Login with cookies
    content = ''
    try:
        cookies = SimpleCookie()
        cookies.load(raw_cookies)
        result = session_requests.get(main_url, cookies={k: v.value for k, v in cookies.items()})
        content = result.text
    except Exception as e:
        pass

    if username in result.text:
        m = re.findall(r'积分: (\d+)', content)
        point = m[0]
        return int(point)

    else:
        return None


# Info
now = date.today()
point = login_with_cookies(username, raw_cookies)

if point is None:
    print(f'[1point] x')
    print('---')
    print(f'{now.isoformat()} ')
else:
    print(f'[1point] {point}')
    print('---')
    print(f'{now.isoformat()} ')
