import random
import string

from .models import URLMap
from .constants import RANGE_NUMBER


def get_short(short):
    if short:
        return short
    symbols = string.ascii_letters + string.digits
    while True:
        new_short = ''.join((random.choice(symbols) for _ in range(RANGE_NUMBER)))
        if URLMap.query.filter_by(short=new_short).first() is None:
            return new_short
