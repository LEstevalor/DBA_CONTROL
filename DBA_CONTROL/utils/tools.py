import re

from rest_framework import status
from rest_framework.response import Response

from cmts.models import Teacher


def is_valid_email(email):
    """判断是否为合法邮箱"""
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return pattern.match(email)


def check_teach_name_and_id(cursor, teach_id, teacher_name=None):
    """传入connection和教师名称、教师ID，检查ID是否存在，id和name是否匹配得上，如果存在则不返回，不存在则报错404"""
    message = ''
    if teacher_name:
        cursor.execute("select content from gdut_teacher where id = '%s' and name = '%s'" % (teach_id, teacher_name))
        message = "教师ID不存在或教师名称与教师ID匹配不上"
    else:
        cursor.execute("select content from gdut_teacher where id = '%s'" % teach_id)
        message = "教师ID不存在"
    if cursor.fetchone() is None:
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
