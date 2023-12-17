from flask import flash, redirect, render_template, url_for
from wtforms import ValidationError

from . import app, SHORT_LINK_FUNCTION
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=('GET', 'POST',))
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            url=url_for(
                SHORT_LINK_FUNCTION,
                short_id=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data,
                    validate=False
                ).short,
                _external=True)
        )
    except (ValidationError, ValueError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=('GET',))
def short_link_url(short_id):
    url_map = URLMap.is_short_link_exists(short_id, get_404=True)
    return redirect(url_map.original)
