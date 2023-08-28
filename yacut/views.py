from flask import redirect, render_template, flash, abort

from . import app, db
from .forms import URLMapForm
from .models import URLMap, get_short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    urlmap = None

    if form.validate_on_submit():
        urlmap = URLMap(
            original=form.original_link.data,
            short=get_short(form.custom_id.data)
        )

        if URLMap.query.filter_by(short=form.custom_id.data).first() is not None:
            flash(f'Имя {form.custom_id.data} уже занято!')
            return render_template('index.html', form=form)
        db.session.add(urlmap)
        db.session.commit()
        return render_template(
            'index.html', form=form, slug=urlmap.short)

    return render_template('index.html', form=form)


@app.route('/<string:slug>')
def short_url_view(slug):
    url = URLMap.query.filter_by(short=slug).first()
    if url is None:
        abort(404)
    return redirect(url.original)
