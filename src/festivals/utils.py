import datetime

import pytz


APRIL_FOOL_COOKIE_KEY = 'april_fool_hahaha_uccu_uccu'
APRIL_FOOL_COOKIE_DONE_VALUE = '1'


def get_tomorrow():
    tomorrow = (
        (datetime.datetime.today() + datetime.timedelta(days=1))
        .replace(tzinfo=pytz.timezone('Asia/Taipei'))
        .astimezone(pytz.UTC)
    )
    return tomorrow
