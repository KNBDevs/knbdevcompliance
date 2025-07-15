# app/routes/fichajes.py

from flask import Blueprint, render_template, redirect, url_for, Response, flash, request
from flask_login import login_required
from app.models import Fichaje, Trabajador
from app import db
import csv
from io import StringIO

bp = Blueprint('fichajes', __name__, url_prefix='/fichajes')

@bp.route('/')
@login_required
def lista_fichajes():
    from sqlalchemy import desc, asc

    sort = request.args.get('sort')
    order = request.args.get('order', 'desc')

    sort_column = {
        'fecha': Fichaje.fecha,
        'hora': Fichaje.hora,
        'tipo': Fichaje.tipo,
        'trabajador': Trabajador.nombre,
        'centro': Trabajador.centro_id
    }.get(sort, Fichaje.fecha)  # default: fecha

    query = db.session.query(Fichaje).join(Fichaje.trabajador)

    if order == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # Segundo orden secundario si es necesario (e.g. hora después de fecha)
    if sort != 'hora':
        query = query.order_by(sort_column, Fichaje.hora.desc() if order == 'desc' else Fichaje.hora.asc())

    fichajes = query.all()
    return render_template('lista_fichajes.html', fichajes=fichajes)


@bp.route('/trabajador/<int:trabajador_id>')
@login_required
def historial_fichajes(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)
    fichajes = Fichaje.query.filter_by(trabajador_id=trabajador.id)\
                            .order_by(Fichaje.fecha.desc(), Fichaje.hora.desc()).all()
    return render_template('fichajes.html', trabajador=trabajador, fichajes=fichajes)

@bp.route('/exportar/csv')
@login_required
def exportar_fichajes_csv():
    fichajes = Fichaje.query.order_by(Fichaje.fecha.desc(), Fichaje.hora.desc()).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Fecha', 'Hora', 'Tipo', 'Trabajador'])

    for f in fichajes:
        writer.writerow([
            f.fecha.strftime('%Y-%m-%d'),
            f.hora.strftime('%H:%M:%S'),
            f.tipo,
            f.trabajador.nombre
        ])

    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=fichajes.csv"}
    )

@bp.route('/<int:trabajador_id>/exportar/csv')
@login_required
def exportar_fichajes_trabajador_csv(trabajador_id):
    fichajes = Fichaje.query.filter_by(trabajador_id=trabajador_id)\
                            .order_by(Fichaje.fecha.desc(), Fichaje.hora.desc()).all()

    if not fichajes:
        flash('Este trabajador no tiene fichajes para exportar.', 'warning')
        return redirect(url_for('fichajes.historial_fichajes', trabajador_id=trabajador_id))

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Fecha', 'Hora', 'Tipo'])

    for f in fichajes:
        writer.writerow([
            f.fecha.strftime('%Y-%m-%d'),
            f.hora.strftime('%H:%M:%S'),
            f.tipo
        ])

    output = si.getvalue()
    si.close()

    nombre_archivo = f"fichajes_{fichajes[0].trabajador.nombre.replace(' ', '_').lower()}.csv"

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={nombre_archivo}"}
    )
