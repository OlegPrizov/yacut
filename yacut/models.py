from datetime import datetime
from random import choice
from flask import url_for
import string

from . import db
ALLOWED_SYMBOLS = string.ascii_letters + string.digits


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'short_link_url', short_id=self.short, _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def is_short_link_exists(self, custom_id):
        return bool(
            self.query.filter_by(short=custom_id).first()
        )

    def get_unique_short_id(self):
        result_short_id = ''
        while len(result_short_id) != 6:
            result_short_id += choice(ALLOWED_SYMBOLS)

        if not self.is_short_link_exists(result_short_id):
            return result_short_id
        return self.get_unique_short_id()

    def is_valid_short_id(self, short_id):
        if len(short_id) > 16:
            return False
        for value in short_id:
            if value not in ALLOWED_SYMBOLS:
                return False
        return True