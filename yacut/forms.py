from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    MAX_SHORT_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    SHORT_PATTERN
)

ORIGINAL_LINK_NAME = 'Длинная ссылка'
CUSTOM_LINK_NAME = 'Ваш вариант короткой ссылки'
REQUIRED_DATA_MESSAGE = 'Обязательное поле'
SUBMIT_MESSAGE = 'Создать'


class UrlForm(FlaskForm):
    original_link = StringField(
        ORIGINAL_LINK_NAME,
        validators=[
            DataRequired(message=REQUIRED_DATA_MESSAGE),
            Length(max=MAX_ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        CUSTOM_LINK_NAME,
        validators=[
            Length(max=MAX_SHORT_LENGTH),
            Regexp(SHORT_PATTERN),
            Optional(),
        ]
    )
    submit = SubmitField(SUBMIT_MESSAGE)
