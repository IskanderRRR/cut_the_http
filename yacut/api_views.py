import re

from flask import jsonify, request

from . import app, db
from .models import URLMap, get_short
from .error_handlers import APIErrors


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise APIErrors('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not data or data == {}:
        raise APIErrors('Отсутствует тело запроса')

    if 'url' not in data:
        raise APIErrors('\"url\" является обязательным полем!')

    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if not re.match('^[a-zA-Z0-9]*$', custom_id) or len(custom_id) > 16:
            raise APIErrors('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise APIErrors(f'Имя "{custom_id}" уже занято.')

    urlmap = URLMap(
        original=data.get('url'),
        short=get_short(data.get('custom_id'))
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
