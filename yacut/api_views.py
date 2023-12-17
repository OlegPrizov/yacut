from http import HTTPStatus

from flask import jsonify, request
from wtforms import ValidationError

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'
NO_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_MESSAGE = '"url" является обязательным полем!'


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    url_map = URLMap.is_short_link_exists(short_id)
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(ID_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=('POST',))
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_BODY_MESSAGE)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_MESSAGE)
    try:
        return jsonify(
            URLMap.create(
                data.get('url'),
                data.get('custom_id'),
                validate=True
            ).to_dict()), HTTPStatus.CREATED
    except (ValidationError, ValueError) as error:
        raise InvalidAPIUsage(str(error))
