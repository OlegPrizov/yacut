from datetime import datetime
from random import choices

from flask import url_for
from wtforms import ValidationError

from . import db, SHORT_LINK_FUNCTION
from .constants import (
    ALLOWED_SYMBOLS,
    CUSTOM_LINK_PATTERN,
    MAX_AUTOGENERATE_CUSTOM_LINK_LENGTH,
    MAX_CUSTOM_LINK_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    MAX_ITERATIONS
)

SHORT_LINK_EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
ERROR_MESSAGE = 'Невозможно сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_CUSTOM_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def is_short_link_exists(custom_id: str, get_404=False):
        if get_404:
            return URLMap.query.filter_by(short=custom_id).first_or_404()
        return URLMap.query.filter_by(short=custom_id).first()

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                SHORT_LINK_FUNCTION, short_id=self.short, _external=True
            )
        )

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_ITERATIONS):
            result_short_id = ''.join(choices(
                ALLOWED_SYMBOLS,
                k=MAX_AUTOGENERATE_CUSTOM_LINK_LENGTH
            ))
            if not URLMap.is_short_link_exists(result_short_id):
                return result_short_id
        raise ValueError(ERROR_MESSAGE)

    @staticmethod
    def is_valid_short_id(short_id):
        if len(short_id) > MAX_CUSTOM_LINK_LENGTH:
            raise ValidationError
        if not CUSTOM_LINK_PATTERN.match(short_id):
            raise ValidationError
        return short_id

    @staticmethod
    def create(url: str, short: str, validate: bool):
        if not short:
            short = URLMap.get_unique_short_id()
        elif URLMap.is_short_link_exists(short):
            raise ValidationError(SHORT_LINK_EXISTS_MESSAGE)
        if validate:
            try:
                URLMap.is_valid_short_id(short) == short
            except ValidationError:
                raise ValidationError(INVALID_SHORT_ID_MESSAGE)
        new_data = URLMap(original=url, short=short)
        db.session.add(new_data)
        db.session.commit()
        return new_data
