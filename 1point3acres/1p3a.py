#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import requests
import re
import base64
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from urllib.parse import urljoin
from local_settings import username, raw_cookies
from dataclasses import dataclass


MAIN_URL = 'https://www.1point3acres.com/bbs/'
PROFILE_URL = "https://www.1point3acres.com/bbs/home.php?mod=spacecp&ac=credit&showcredit=1"
DAY_QUESTION_URL = 'https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop&infloat=yes&handlekey=pop&inajax=1&ajaxtarget=fwin_content_pop'


@dataclass
class Profile:
    username: str = ''
    point: int = 0
    day_question_status: bytes = bytes()
    day_question: str = None
    error: Exception = None


def login_with_cookies(username, raw_cookies):
    # Utils
    session_requests = requests.session()
    profile = Profile()

    # Login with cookies
    try:
        cookies = SimpleCookie()
        cookies.load(raw_cookies)
        cookies = {k: v.value for k, v in cookies.items()}
        result = session_requests.get(MAIN_URL, cookies=cookies)

        if username not in result.text:
            return None
        result = session_requests.get(PROFILE_URL, cookies=cookies)

        # Parse point
        m = re.findall(r'积分: (\d+)', result.text)
        profile.point = int(m[0])

        # Parse day question status
        soup = BeautifulSoup(result.text, features="html.parser")
        img = soup.find('img', src=re.compile("source/plugin/ahome_dayquestion/images/.*"))
        image_url = img.attrs['src']
        profile.day_question_status = base64.b64encode(session_requests.get(urljoin(MAIN_URL, image_url)).content)

        # Parse day question
        result = session_requests.get(DAY_QUESTION_URL, cookies=cookies)
        if '参加过答题' not in result.text:
            # TODO
            html = result.text
            print(html)
            profile.day_question = html

        return profile

    except Exception as e:
        profile.error = e
        return profile


def bitbar_menu():
    # Info
    profile = login_with_cookies(username, raw_cookies)
    icon_b64 = """
    AAABAAEAEBAAAAAAAABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/s2JRq0qIA/9KiAP/duD7A////AP///wD///8A////AP///wD///8A////AP///wD///8A7NiUatKiAP////8A0qIA/9KiAP/SogD/0qIA/////wD///8A////AP///wD///8A////AP///wD///8A////ANKiAP/SogD/////ANKiAP/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/////wDgwFSq0qIA/9KiAP////8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/SogD/0qIA/9KiAP/SogD/////AP///wDSogD/0qIA/////wD///8A////AP///wD///8A0qIA/9KiAP/SogD/////AP///wDSogD/////AP///wD///8A0qIA/9KiAP////8A0qIA/+TIapT///8A////AP///wD///8A1akU6tKiAP/SogD/0qIA/////wD///8A////AOvVjXHSogD/////ANKiAP/SogD/0qIA/9KiAP////8A////AP///wD///8A////ANKiAP/SogD/0qIA/9KiAP/SogD/7NiUav///wDUpw/v0qIA/9KiAP/SogD/0qIA/9SnD+////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////APz57w/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A6NB/f9KiAP/SogD/0qIA/9WpFenSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD79+oU0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ANmxKtTz578/////AP///wD///8A////AP///wD///8A//8AAPyPAAD9DwAA+QcAAPkTAAD4GQAA8bkAADw9AAAPgwAAA/8AAPh/AAD/gAAA//EAAP+fAAD/HwAA/38AAA==
    """

    if profile.error is not None:
        print(f'x | image={icon_b64.strip()}')
        print('---')
        print(f'Error')
        print(f'--{repr(profile.error)}')
    else:
        print(f' | image={icon_b64.strip()}')
        print('---')
        print(f'{profile.point}')
        print(f'| image={profile.day_question_status.decode("utf-8")} href={MAIN_URL}')
        if profile.day_question:
            print('Day Question')
            print(f'--{profile.day_question}')


if __name__ == "__main__":
    bitbar_menu()
