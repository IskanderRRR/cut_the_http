from datetime import datetime
from flask import url_for

import random
import string

from . import db


def get_short(short):
    if short and short != '':
        return short
    symbols = string.ascii_letters + string.digits
    while True:
        new_short = ''.join((random.choice(symbols) for _ in range(6)))
        if URLMap.query.filter_by(short=new_short).first() is None:
            return new_short


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(512), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('short_url_view', slug=self.short, _external=True)
        )
