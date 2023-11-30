from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=('POST',))
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    url_map = URLMap()
    custom_id = data.get('custom_id', None)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if not custom_id or custom_id is None:
        custom_id = url_map.get_unique_short_id()
        data.update({'custom_id': custom_id})

    if url_map.is_short_link_exists(custom_id):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if not url_map.is_valid_short_id(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)