from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    MAX_CUSTOM_LINK_LENGTH,
    MAX_ORIGINAL_LINK_LENGTH,
    CUSTOM_LINK_PATTERN
)

ORIGINAL_LINK_NAME = 'Длинная ссылка'
CUSTOM_LINK_NAME = 'Ваш вариант короткой ссылки'
REQUIRED_DATA_MESSAGE = 'Обязательное поле'


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
            Length(max=MAX_CUSTOM_LINK_LENGTH),
            Regexp(CUSTOM_LINK_PATTERN),
            Optional(),
        ]
    )
    submit = SubmitField('Создать')
