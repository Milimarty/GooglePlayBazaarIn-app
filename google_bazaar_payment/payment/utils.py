import datetime
from django.conf import settings


def logger(*args):
    if settings.DEBUG:
        now_time = datetime.datetime.now().strftime('%H:%M:%S')
        now_date = datetime.datetime.now().strftime('%d/%m/%Y')
        print("*" * 35)
        print(f"[{now_date} {now_time}]", args)
        print("*" * 35)
