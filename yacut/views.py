from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        custom_id = form.custom_id.data
        existing_urlmap = URLMap.query.filter_by(short=custom_id).first()
        if existing_urlmap:
            flash(f'Имя {custom_id} уже занято!')
        else:
            urlmap = URLMap(
                original=form.original_link.data,
                short=get_short(custom_id)
            )
            db.session.add(urlmap)
            db.session.commit()
            return render_template('index.html', form=form, slug=urlmap.short)

    return render_template('index.html', form=form)


@app.route('/<string:slug>')
def short_url_view(slug):
    url = URLMap.query.filter_by(short=slug).first_or_404()
    return redirect(url.original)
