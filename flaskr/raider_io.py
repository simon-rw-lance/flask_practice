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
    chars = db.execute(
        'SELECT p.id, region, realm, char_name, score'
        ' FROM wow_char p JOIN user u ON p.author_id = u.id'
        ' ORDER BY realm, char_name'
        ).fetchall()
    return render_template('raider_io/index.html', wow_chars=chars)

@bp.route('/raider_io/new', methods=('GET', 'POST'))
@login_required
def new():
    if request.method == 'POST':
        region = request.form['region'].lower()
        realm = request.form['realm']
        char_name = request.form['char_name']

        error = None

        if not region in ['eu','us', 'EU', 'US']:
            error = 'Incorrect region selected. Only EU and US allowed.'

        db = get_db()
        chars = db.execute('SELECT region, realm, char_name, score FROM wow_char').fetchall()

        for row in chars:
            if ((region==row[0]) and (realm==row[1]) and (char_name==row[2])):
                error = "Character already loaded."

        from . import raider_calc
        # First attempt at catching errors with the API call. More specific ones should
        # be added to the function raider_calc itself when that is rewritten.
        try:
            score = raider_calc.GetScore(region, realm, char_name)
        except:
            error = "Issue detected with API call. Please check the information provided."
        else:
            score = raider_calc.GetScore(region, realm, char_name)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO wow_char (region, realm, char_name, score, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (region, realm, char_name, score, g.user['id'])
            )
            db.commit()
            return redirect(url_for('raider_io.index'))

    return render_template('raider_io/new.html')
