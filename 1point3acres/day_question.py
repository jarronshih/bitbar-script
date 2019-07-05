DAY_QUESTIONS = [("【题目】 下面哪个州，没有state income tax?", ("New Hampshire",))]


def parse_option(option_soup):
    return option_soup.find("input").attrs["value"]


def day_question_answer(question, options):
    for q, a in DAY_QUESTIONS:
        if q == question:
            for aa in a:
                for option in options:
                    if aa in option.text:
                        return (option, parse_option(option))
    return None
