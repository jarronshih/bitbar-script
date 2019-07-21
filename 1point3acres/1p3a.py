#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
import requests
import re
import base64
import bs4
import googlesearch
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from urllib.parse import urljoin
from local_settings import username, raw_cookies
from dataclasses import dataclass


MAIN_URL = "https://www.1point3acres.com/bbs/"
PROFILE_URL = (
    "https://www.1point3acres.com/bbs/home.php?mod=spacecp&ac=credit&showcredit=1"
)
DAY_QUESTION_URL = "https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop&infloat=yes&handlekey=pop&inajax=1&ajaxtarget=fwin_content_pop"
DAY_QUESTION_POST_URL = (
    "https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop"
)
CHECKIN_URL = "https://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign"
CHECKIN_POST_URL = "https://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0"

ICON_B64 = """
AAABAAEAEBAAAAAAAABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/s2JRq0qIA/9KiAP/duD7A////AP///wD///8A////AP///wD///8A////AP///wD///8A7NiUatKiAP////8A0qIA/9KiAP/SogD/0qIA/////wD///8A////AP///wD///8A////AP///wD///8A////ANKiAP/SogD/////ANKiAP/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/////wDgwFSq0qIA/9KiAP////8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP/SogD/0qIA/9KiAP/SogD/////AP///wDSogD/0qIA/////wD///8A////AP///wD///8A0qIA/9KiAP/SogD/////AP///wDSogD/////AP///wD///8A0qIA/9KiAP////8A0qIA/+TIapT///8A////AP///wD///8A1akU6tKiAP/SogD/0qIA/////wD///8A////AOvVjXHSogD/////ANKiAP/SogD/0qIA/9KiAP////8A////AP///wD///8A////ANKiAP/SogD/0qIA/9KiAP/SogD/7NiUav///wDUpw/v0qIA/9KiAP/SogD/0qIA/9SnD+////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////APz57w/SogD/0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A6NB/f9KiAP/SogD/0qIA/9WpFenSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDSogD/0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A0qIA/9KiAP////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD79+oU0qIA/9KiAP/SogD/////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////ANmxKtTz578/////AP///wD///8A////AP///wD///8A//8AAPyPAAD9DwAA+QcAAPkTAAD4GQAA8bkAADw9AAAPgwAAA/8AAPh/AAD/gAAA//EAAP+fAAD/HwAA/38AAA==
""".strip()

DAY_QUESTIONS = [
    ("下面哪个州，没有state income tax", ("New Hampshire", "Florida", "Alaska", "Nevada", "South Dakota", "Texas", "Washington", "Wyoming")),
    ("下面哪种行为，在地里会被扣光积分，甚至封号", ("这些全都会",)),
    ("下面哪类版块，可以拉群，而且不会被警告扣分", ("学友工友、找室友或者版聚本地",)),
    ("一亩三分地是哪年创立的", ("2009",)),
    ("下面哪个大学不在Virginia/DC附近", ("Washington and Jefferson College",)),
    ("下面哪所大学所在城市不是波士顿", ("Boston College",)),
    ("下面哪种情况，管理员会按照你的要求，进行删帖", ("这些情况全都不删帖！",)),
    ("地里发帖可以隐藏内容", ("[hide=200]想要隐藏的内容[/hide]",)),
    ("哪种选校策略最合理", ("根据自己下一步职业和学业目标，参考地里数据和成功率，认真斟酌",)),
    # ("", ("",)),
]


def parse_option(option_soup):
    return option_soup.find("input").attrs["value"]


def day_question_answer(question, options):
    # Search from db
    for q, a in DAY_QUESTIONS:
        if q in question:
            for aa in a:
                for option in options:
                    if aa in option.text:
                        return (option, parse_option(option))

    # Search by google
    # return max(options, key=lambda option: googlesearch.hits(f'{question} {option.text}'))

    return (None, None)


@dataclass
class Profile:
    username: str = ""
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
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
        result = session_requests.get(MAIN_URL, cookies=cookies)

        if username not in result.text:
            return None
        result = session_requests.get(PROFILE_URL, cookies=cookies, headers=headers)

        # Parse point
        m = re.findall(r"积分: (\d+)", result.text)
        profile.point = int(m[0])

        # Auto check-in
        if "签到领奖" in result.text:
            result = session_requests.get(CHECKIN_URL, cookies=cookies, headers=headers)
            soup = BeautifulSoup(result.text, features="html.parser")
            formhash = soup.find("input", {"name": "formhash"})
            qdxq = soup.find("ul", {"class": "qdsmile"}).find("input", {"name": "qdxq"})
            data = {
                "formhash": formhash.attrs["value"],
                "qdxq": qdxq.attrs["value"],
                "qdmode": 2,
                "todaysay": "",
                "fastreply": 1,
            }
            response = requests.post(
                CHECKIN_POST_URL, data=data, cookies=cookies, headers=headers
            )
            # assert '签到成功' in response.text

        # Parse day question status
        soup = BeautifulSoup(result.text, features="html.parser")
        img = soup.find(
            "img", src=re.compile("source/plugin/ahome_dayquestion/images/.*")
        )
        image_url = img.attrs["src"]
        profile.day_question_status = base64.b64encode(
            session_requests.get(urljoin(MAIN_URL, image_url)).content
        )

        # Parse day question
        result = session_requests.get(
            DAY_QUESTION_URL, cookies=cookies, headers=headers
        )
        if "参加过答题" not in result.text:
            # print(result.text)
            soup = BeautifulSoup(result.text, features="html.parser")
            cdata = soup.find(
                text=lambda tag: isinstance(tag, bs4.CData)
            ).string.strip()

            soup = BeautifulSoup(cdata, features="html.parser")
            qs = soup.find("font")
            qs_options = soup.findAll("div", {"class": "qs_option"})

            if qs and qs_options:
                profile.day_question = qs.text
                answer_soup, answer_value = day_question_answer(qs.text, qs_options)
                if answer_soup:
                    profile.day_question += f": {answer_soup.text}"
                    # Submit answer
                    #  - <input type="hidden" name="formhash" value="4c1c91f5">
                    #  - <input type="radio" id="a1" name="answer" value="1">
                    formhash = soup.find("input", {"name": "formhash"})
                    data = {
                        "formhash": formhash.attrs["value"],
                        "answer": answer_value,
                        "submit": True,
                    }
                    response = requests.post(
                        DAY_QUESTION_POST_URL,
                        data=data,
                        cookies=cookies,
                        headers=headers,
                    )
                    # assert '???' in response.text

        return profile

    except Exception as e:
        profile.error = e
        return profile


def bitbar_menu():
    # Info
    profile = login_with_cookies(username, raw_cookies)
    # return

    if profile.error is not None:
        print(f"x | image={ICON_B64}")
        print("---")
        print(f"Error")
        print(f"--{repr(profile.error)}")
    else:
        print(f" | image={ICON_B64}")
        print("---")
        print(f"{profile.point}")
        print(f'| image={profile.day_question_status.decode("utf-8")} href={MAIN_URL}')
        if profile.day_question:
            print("Day Question")
            print(f"--{profile.day_question}")


if __name__ == "__main__":
    bitbar_menu()
