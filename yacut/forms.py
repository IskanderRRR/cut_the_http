from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .constants import CUSTOM_ID_REGEX, MAX_CUSTOM_ID_LENGTH


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Адрес URL',
        description='https://example.com',
        validators=[
            DataRequired(message='Обязательное поле.'),
            URL(message='Некорректный адрес URL.'),
        ],
    )
    custom_id = StringField(
        'Короткая ссылка',
        description='Длина не более 16 символов, латинские буквы и цифры',
        validators=[
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message='Длина поля не должна превышать 16 символов.',
            ),
            Regexp(
                CUSTOM_ID_REGEX,
                message=(
                    'Идентификатор может состоять только из латинских букв и цифр.'
                ),
            ),
            Optional()
        ],
    )
    submit = SubmitField('Создать')
