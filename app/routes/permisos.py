# app/routes/permisos.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Vacacion, Trabajador
from app import db
from flask_babel import gettext as _
from datetime import datetime

bp = Blueprint('permisos', __name__, url_prefix='/permisos')


@bp.route('/')
@login_required
def lista_permisos():
    from sqlalchemy import asc, desc

    sort = request.args.get('sort', 'fecha_inicio')
    order = request.args.get('order', 'desc')

    sort_column = {
        'trabajador': Trabajador.nombre,
        'desde': Vacacion.fecha_inicio,
        'hasta': Vacacion.fecha_fin,
        'estado': Vacacion.estado,
        'justificacion': Vacacion.justificacion
    }.get(sort, Vacacion.fecha_inicio)

    query = db.session.query(Vacacion).join(Trabajador)

    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    permisos = query.all()
    return render_template('lista_permisos.html', permisos=permisos)



@bp.route('/aprobar/<int:permiso_id>')
@login_required
def aprobar_permiso(permiso_id):
    permiso = Vacacion.query.get_or_404(permiso_id)
    permiso.estado = 'aceptada'
    db.session.commit()
    flash(_('Permiso aprobado.'), 'success')
    return redirect(url_for('permisos.lista_permisos'))


@bp.route('/rechazar/<int:permiso_id>')
@login_required
def rechazar_permiso(permiso_id):
    permiso = Vacacion.query.get_or_404(permiso_id)
    permiso.estado = 'rechazada'
    db.session.commit()
    flash(_('Permiso rechazado.'), 'danger')
    return redirect(url_for('permisos.lista_permisos'))


@bp.route('/nuevo/<int:trabajador_id>', methods=['GET', 'POST'])
@login_required
def nuevo_permiso(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)

    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        justificacion = request.form.get('justificacion')

        try:
            permiso = Vacacion(
                trabajador_id=trabajador.id,
                fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
                fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d'),
                justificacion=justificacion,
                estado='pendiente'
            )
            db.session.add(permiso)
            db.session.commit()
            flash('Permiso creado correctamente.', 'success')
            return redirect(url_for('permisos.lista_permisos'))
        except Exception as e:
            flash('Error al crear el permiso.', 'danger')
            print(e)

    return render_template('nuevo_permiso.html', trabajador=trabajador)

@bp.route('/<int:trabajador_id>')
@login_required
def permisos_trabajador(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)
    permisos = Vacacion.query.filter_by(trabajador_id=trabajador.id).order_by(Vacacion.fecha_inicio.desc()).all()
    return render_template('permisos.html', trabajador=trabajador, permisos=permisos)
