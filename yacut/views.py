from flask import flash, redirect, render_template, url_for

from . import app, db, SHORT_LINK_FUNCTION
from .forms import UrlForm
from .models import URLMap

@app.route('/', methods=('GET', 'POST',))
def index_view():
    form = UrlForm()
    url_to_template = None

    if not form.validate_on_submit():
        return render_template('index.html', form=form, url=None)

    url_map = URLMap()
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = url_map.get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        flash('Предложенный вариант короткой ссылки уже существует.', 'rejected')
    elif not url_map.is_valid_short_id(custom_id):
        flash("Ваша короткая ссылка содержит недопустимые символы.", 'rejected')
    else:
        short_url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(short_url)
        db.session.commit()
        url_to_template = url_for(SHORT_LINK_FUNCTION, short_id=custom_id, _external=True)

    return render_template('index.html', form=form, url=url_to_template)



@app.route('/<string:short_id>', methods=('GET',))
def short_link_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
