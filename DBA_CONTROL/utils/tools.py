import re


def is_valid_email(email):
    """判断是否为合法邮箱"""
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return pattern.match(email)
