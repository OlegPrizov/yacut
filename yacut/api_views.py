from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap

ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'
NO_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_MESSAGE = '"url" является обязательным полем!'
SHORT_LINK_EXISTS_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'

# @app.route('/api/id/', methods=('POST',))
# def add_short_url():
#     data = request.get_json()
#     if not data:
#         raise InvalidAPIUsage(NO_BODY_MESSAGE)
#     if 'url' not in data:
#         raise InvalidAPIUsage(NO_URL_MESSAGE)
#     try:
#         url_map = URLMap()
#         custom_id = data.get('custom_id', None)
#         if not custom_id or custom_id is None:
#             custom_id = url_map.get_unique_short_id()
#         if url_map.is_short_link_exists(custom_id):
#             raise InvalidAPIUsage(SHORT_LINK_EXISTS_MESSAGE)
#         if not url_map.is_valid_short_id(custom_id):
#             raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
#         else:
#             short_url = URLMap(
#                 original = data.get('url'),
#                 short = custom_id
#             )
#     except Exception as error:
#         return jsonify({'message': str(error)}), HTTPStatus.BAD_REQUEST
#     return jsonify(short_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_short_url(short_id):
    url_map = URLMap.get_original_url(short_id)
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage(ID_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)

@app.route('/api/id/', methods=('POST',)) 
def add_short_url(): 
    data = request.get_json() 
    if not data: 
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data: 
        raise InvalidAPIUsage('"url" является обязательным полем!')
    url = data.get('url')
    custom_id = data.get('custom_id', None)
    try:
        jsonify(URLMap.save(url, custom_id).to_dict()), HTTPStatus.CREATED
    except Exception as error:
        raise InvalidAPIUsage(str(error))
