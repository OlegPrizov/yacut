from flask import flash, redirect, render_template, url_for
from wtforms import ValidationError

from . import app, SHORT_LINK_FUNCTION
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=('GET', 'POST',))
def index_view():
    form = UrlForm()
    url_to_template = None

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    try:
        url_to_template = url_for(
            SHORT_LINK_FUNCTION,
            short_id=URLMap.save(
                form.original_link.data,
                form.custom_id.data
            ).short,
            _external=True)
        return render_template(
            'index.html',
            form=form,
            url=url_to_template
        )
    except (ValidationError, ValueError) as error:
        flash(str(error), 'rejected')
        return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=('GET',))
def short_link_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
