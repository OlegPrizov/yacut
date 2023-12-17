from datetime import datetime
from random import choices
import re

from flask import url_for
from .error_handlers import InvalidAPIUsage
from . import db, SHORT_LINK_FUNCTION
from .constants import (
    ALLOWED_SYMBOLS,
    MAX_AUTOGENERATE_CUSTOM_LINK_LENGTH,
    MAX_CUSTOM_LINK_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    PATTERN
)

SHORT_LINK_EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
NO_BODY_MESSAGE = 'Отсутствует тело запроса'

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_CUSTOM_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def is_short_link_exists(self, custom_id):
        return bool(
            self.query.filter_by(short=custom_id).first()
        )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                SHORT_LINK_FUNCTION, short_id=self.short, _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def get_unique_short_id(self):
        result_short_id = ''
        result_short_id += "".join(choices(ALLOWED_SYMBOLS, k=MAX_AUTOGENERATE_CUSTOM_LINK_LENGTH))

        while self.is_short_link_exists(result_short_id) == True:
            self.get_unique_short_id()
        
        return result_short_id

    def is_valid_short_id(self, short_id):
        if len(short_id) > MAX_CUSTOM_LINK_LENGTH:
            return False
        if not re.match(PATTERN, short_id):
            return False
        return True

    def get_original_url(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def save(url, short, check_short=True):
        if not custom_id or custom_id is None:
            custom_id = URLMap.get_unique_short_id()
        if URLMap.is_short_link_exists(custom_id):
            raise InvalidAPIUsage(SHORT_LINK_EXISTS_MESSAGE)
        if not URLMap.is_valid_short_id(custom_id):
            raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
        new_data = URLMap(
            original = url,
            short = short
        )
        db.session.add(new_data)
        db.session.commit()
        return new_data
