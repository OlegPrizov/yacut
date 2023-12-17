from datetime import datetime
from random import choices

from flask import url_for
from wtforms import ValidationError

from . import db, SHORT_FUNCTION
from .constants import (
    ALLOWED_SYMBOLS,
    SHORT_PATTERN,
    MAX_AUTOGENERATE_SHORT_LENGTH,
    MAX_SHORT_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    MAX_ITERATIONS
)

SHORT_EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
ERROR_SHORT_GENERATE_MESSAGE = 'Невозможно сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_ORIGINAL_LINK_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short: str, get_404=False):
        if get_404:
            return URLMap.query.filter_by(short=short).first_or_404()
        return URLMap.query.filter_by(short=short).first()

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                SHORT_FUNCTION, short=self.short, _external=True
            )
        )

    @staticmethod
    def get_unique_short():
        for _ in range(MAX_ITERATIONS):
            short = ''.join(choices(
                ALLOWED_SYMBOLS,
                k=MAX_AUTOGENERATE_SHORT_LENGTH
            ))
            if not URLMap.get(short):
                return short
        raise ValueError(ERROR_SHORT_GENERATE_MESSAGE)

    @staticmethod
    def is_short_valid(short: str):
        if len(short) > MAX_SHORT_LENGTH:
            raise ValidationError(INVALID_SHORT_MESSAGE)
        if not SHORT_PATTERN.match(short):
            raise ValidationError(INVALID_SHORT_MESSAGE)
        return short

    @staticmethod
    def create(url, short, validate: bool):
        if not short:
            short = URLMap.get_unique_short()
        elif URLMap.get(short):
            raise ValidationError(SHORT_EXISTS_MESSAGE)
        elif validate:
            URLMap.is_short_valid(short)
        new_data = URLMap(original=url, short=short)
        db.session.add(new_data)
        db.session.commit()
        return new_data
