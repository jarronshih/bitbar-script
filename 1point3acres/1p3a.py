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
    try:
        cookies = SimpleCookie()
        cookies.load(raw_cookies)
        cookies = {k: v.value for k, v in cookies.items()}
        result = session_requests.get(MAIN_URL, cookies=cookies)

        if username not in result.text:
            return None
        result = session_requests.get("https://www.1point3acres.com/bbs/home.php?mod=spacecp&ac=credit&showcredit=1", cookies=cookies)

        profile = Profile()
        m = re.findall(r'积分: (\d+)', result.text)
        profile.point = int(m[0])

        soup = BeautifulSoup(result.text, features="html.parser")

        a = soup.find('a', onclick="showWindow('pop','plugin.php?id=ahome_dayquestion:pop')")
        if not a:
            a = soup.find('a', href="plugin.php?id=ahome_dayquestion:index")

        if a:
            img = a.img
        else:
            img = soup.find('img', id="ahome_question_icon")

        image_url = img.attrs['src']
        profile.day_question = base64.b64encode(session_requests.get(urljoin(MAIN_URL, image_url)).content)
        return profile

    except Exception as e:
        # print(e)
        return profile


# Info
now = date.today()
profile = login_with_cookies(username, raw_cookies)
icon_b64 = """
AAABAAEAEBAAAAAAAABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/s2JRq0qIA/9KiAP/duD7A////AP///wD///8A////AP///wD///8A////AP///wD///8A7NiUatKiAP////8A0qIA/9KiAP/SogD/0qIA/////wD///8A////AP///wD///8A////AP///wD///8A////ANKiAP/SogD/////ANKiAP/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/////wDgwFSq0qIA/9KiAP////8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/SogD/0qIA/9KiAP/SogD/////AP///wDSogD/0qIA/////wD///8A////AP///wD///8A0qIA/9KiAP/SogD/////AP///wDSogD/////AP///wD///8A0qIA/9KiAP////8A0qIA/+TIapT///8A////AP///wD///8A1akU6tKiAP/SogD/0qIA/////wD///8A////AOvVjXHSogD/////ANKiAP/SogD/0qIA/9KiAP////8A////AP///wD///8A////ANKiAP/SogD/0qIA/9KiAP/SogD/7NiUav///wDUpw/v0qIA/9KiAP/SogD/0qIA/9SnD+////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////APz57w/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A6NB/f9KiAP/SogD/0qIA/9WpFenSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD79+oU0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ANmxKtTz578/////AP///wD///8A////AP///wD///8A//8AAPyPAAD9DwAA+QcAAPkTAAD4GQAA8bkAADw9AAAPgwAAA/8AAPh/AAD/gAAA//EAAP+fAAD/HwAA/38AAA==
"""

if profile is None:
    print(f'x | image={icon_b64.strip()}')
    print('---')
    print(f'Error')
else:
    print(f'{profile.point} | image={icon_b64.strip()}')
    print('---')
    print(f'| image={profile.day_question.decode("utf-8")} href={MAIN_URL}')
