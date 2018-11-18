#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import requests
import re
import base64
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from datetime import date
from urllib.parse import urljoin
from local_settings import username, raw_cookies


main_url = 'https://www.1point3acres.com/bbs/'


def login_with_cookies(username, raw_cookies):
    # Utils
    session_requests = requests.session()

    # Login with cookies
    content = ''
    try:
        cookies = SimpleCookie()
        cookies.load(raw_cookies)
        result = session_requests.get(main_url, cookies={k: v.value for k, v in cookies.items()})
        content = result.text

        if username not in result.text:
            return None

        m = re.findall(r'积分: (\d+)', content)
        point = m[0]

        soup = BeautifulSoup(result.text, features="html.parser")
        a = soup.find('a', href="plugin.php?id=ahome_dayquestion:index")
        image_url = a.img.attrs['src']
        image_base64 = base64.b64encode(session_requests.get(urljoin(main_url, image_url)).content)
        return int(point), image_base64

    except Exception as e:
        return None


# Info
now = date.today()
point, image_base64 = login_with_cookies(username, raw_cookies)

if point is None:
    print(f'[1point] x')
    print('---')
    print(f'{now.isoformat()} ')
else:
    print(f'[1point] {point}')
    print('---')
    print(f'{now.isoformat()} ')
    print(f'| image={image_base64.decode("utf-8")} href={main_url}')
