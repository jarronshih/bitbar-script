#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import requests
import re
import base64
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from datetime import date
from urllib.parse import urljoin
from local_settings import username, raw_cookies
from dataclasses import dataclass


MAIN_URL = 'https://www.1point3acres.com/bbs/'


@dataclass
class Profile:
    username: str = ''
    point: int = 0
    day_question: bytes = bytes()


def login_with_cookies(username, raw_cookies):
    # Utils
    session_requests = requests.session()
    profile = None

    # Login with cookies
    content = ''
    try:
        cookies = SimpleCookie()
        cookies.load(raw_cookies)
        result = session_requests.get(MAIN_URL, cookies={k: v.value for k, v in cookies.items()})
        content = result.text

        if username not in result.text:
            return None

        profile = Profile()
        m = re.findall(r'积分: (\d+)', content)
        profile.point = int(m[0])

        soup = BeautifulSoup(result.text, features="html.parser")
        a = soup.find('a', href="plugin.php?id=ahome_dayquestion:index")
        image_url = a.img.attrs['src']
        profile.day_question = base64.b64encode(session_requests.get(urljoin(MAIN_URL, image_url)).content)
        return profile

    except Exception as e:
        print(e)
        return profile


# Info
now = date.today()
profile = login_with_cookies(username, raw_cookies)

if profile is None:
    print(f'[1point] x')
    print('---')
    print(f'{now.isoformat()} ')
else:
    print(f'[1point] {profile.point}')
    print('---')
    print(f'{now.isoformat()} ')
    print(f'| image={profile.day_question.decode("utf-8")} href={MAIN_URL}')
