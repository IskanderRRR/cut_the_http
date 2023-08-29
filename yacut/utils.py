import random
import string
from .models import URLMap

def get_short(short):
    symbols = string.ascii_letters + string.digits
    while True:
        new_short = ''.join((random.choice(symbols) for _ in range(6)))
        if URLMap.query.filter_by(short=new_short).first() is None:
            return new_short
