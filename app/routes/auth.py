# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from app.models import User, Trabajador  # ⬅️ AÑADIDO
from app import db
from flask_babel import gettext as _

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    elif session.get('trabajador_id'):
        return redirect(url_for('fichaje.dashboard'))


    session.pop('_flashes', None)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Primero: intentar login como administrador/responsable
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(_('Bienvenido, ') + user.nombre, 'success')
            return redirect(url_for('dashboard.index'))

        # Segundo: intentar login como trabajador
        trabajador = Trabajador.query.filter_by(email=email, pin=password, activo=True).first()
        if trabajador:
            session.clear()
            session['trabajador_id'] = trabajador.id
            flash(_('Bienvenido, ') + trabajador.nombre, 'success')
            return redirect(url_for('fichaje.dashboard'))

        # Si ambos fallan
        flash(_('Credenciales incorrectas'), 'danger')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash(_('Sesión cerrada correctamente'), 'info')
    return redirect(url_for('auth.login'))
