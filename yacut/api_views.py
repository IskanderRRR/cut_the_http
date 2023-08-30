import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import CUSTOM_ID_REGEX, MAX_CUSTOM_ID_LENGTH
from .error_handlers import APIErrors
from .models import URLMap
from .utils import get_short


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise APIErrors('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not data or data == {}:
        raise APIErrors('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)

    if 'url' not in data:
        raise APIErrors('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)

    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if not re.match(CUSTOM_ID_REGEX, custom_id) or len(custom_id) > MAX_CUSTOM_ID_LENGTH:
            raise APIErrors('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise APIErrors(f'Имя "{custom_id}" уже занято.', HTTPStatus.BAD_REQUEST)

    urlmap = URLMap(
        original=data.get('url'),
        short=get_short(data.get('custom_id'))
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
