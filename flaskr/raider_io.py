from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('raider_io', __name__)

@bp.route('/raider_io')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('raider_io/index.html', posts=posts)
#
# @bp.route('/raider_io')
# def index():
#     db = get_db()
#     posts = db.execute(
#         'SELECT region, realm, character'
#         ).fetchall()
#     return render_template('raider_io/index.html', posts=posts)
#


@bp.route('/raider_io/new', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        region = request.form['region']
        realm = request.form['realm']
        name = request.form['name']

        error = None

        if not region in ['eu','us']:
            error = 'Incorrect region selected. Only EU and US allowed.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (region, realm, character)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('raider_io.index'))

    return render_template('raider_io/new.html')
