from flask import Blueprint, render_template, request, send_file, flash
from flask_login import login_required
from app.models import Trabajador, Horario, Fichaje, Vacacion, Centro
from app import db
from datetime import datetime
import csv
import io

bp = Blueprint('exportar', __name__, url_prefix='/exportar')


@bp.route('/')
@login_required
def panel_exportacion():
    centros = Centro.query.order_by(Centro.nombre).all()
    return render_template('exportar.html', centros=centros)


# -------------------
# EXPORTAR FICHAJES
# -------------------
@bp.route('/fichajes', methods=['POST'])
@login_required
def exportar_fichajes():
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    centro_id = request.form.get('centro')

    fichajes_query = Fichaje.query.join(Trabajador)

    try:
        if fecha_inicio:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fichajes_query = fichajes_query.filter(Fichaje.fecha >= inicio)
        if fecha_fin:
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            fichajes_query = fichajes_query.filter(Fichaje.fecha <= fin)
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return render_template('exportar.html')

    if centro_id:
        try:
            centro_id_int = int(centro_id)
            fichajes_query = fichajes_query.filter(Trabajador.centro_id == centro_id_int)
        except ValueError:
            flash('Centro no válido', 'danger')
            return render_template('exportar.html')

    fichajes = fichajes_query.order_by(Fichaje.fecha, Fichaje.hora).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha', 'Hora', 'Tipo', 'Trabajador', 'Centro'])

    for f in fichajes:
        writer.writerow([
            f.fecha.strftime('%Y-%m-%d'),
            f.hora.strftime('%H:%M:%S'),
            f.tipo,
            f.trabajador.nombre if f.trabajador else 'Desconocido',
            f.trabajador.centro.nombre if f.trabajador and f.trabajador.centro else ''
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='fichajes.csv'
    )


# -------------------
# EXPORTAR HORARIOS
# -------------------
@bp.route('/horarios', methods=['POST'])
@login_required
def exportar_horarios():
    centro_id = request.form.get('centro')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    try:
        inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if fecha_inicio else None
        fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if fecha_fin else datetime.today().date()
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return render_template('exportar.html')

    trabajadores_query = Trabajador.query
    if centro_id:
        trabajadores_query = trabajadores_query.filter(Trabajador.centro_id == centro_id)

    trabajadores = trabajadores_query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Trabajador', 'Centro', 'Día', 'Entrada', 'Salida'])

    for t in trabajadores:
        horarios = Horario.query.filter_by(trabajador_id=t.id).all()
        for h in horarios:
            # Filtrado por fecha ficticio: si quieres vincular esto a una semana real, debes tener fechas reales en Horario.
            if inicio and fin:
                # Aquí no hay fecha en el modelo Horario. Podrías omitir este filtro o adaptar si agregas una columna `fecha`.
                pass

            writer.writerow([
                t.nombre,
                t.centro.nombre if t.centro else '',
                h.dia_semana.capitalize(),
                h.hora_entrada.strftime('%H:%M') if h.hora_entrada else '',
                h.hora_salida.strftime('%H:%M') if h.hora_salida else ''
            ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='horarios.csv'
    )



# -------------------
# EXPORTAR PERMISOS
# -------------------
@bp.route('/permisos', methods=['POST'])
@login_required
def exportar_permisos():
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    centro_id = request.form.get('centro')  # ✅ CORRECTO

    permisos_query = Vacacion.query.join(Trabajador)

    try:
        if fecha_inicio:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            permisos_query = permisos_query.filter(Vacacion.fecha_inicio >= inicio)
        if fecha_fin:
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            permisos_query = permisos_query.filter(Vacacion.fecha_fin <= fin)
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return render_template('exportar.html', centros=Centro.query.order_by(Centro.nombre).all())

    if centro_id:
        try:
            centro_id_int = int(centro_id)
            permisos_query = permisos_query.filter(Trabajador.centro_id == centro_id_int)
        except ValueError:
            flash('Centro no válido', 'danger')
            return render_template('exportar.html', centros=Centro.query.order_by(Centro.nombre).all())

    permisos = permisos_query.order_by(Vacacion.fecha_inicio).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Trabajador', 'Centro', 'Inicio', 'Fin', 'Justificación', 'Estado'])

    for p in permisos:
        writer.writerow([
            p.trabajador.nombre,
            p.trabajador.centro.nombre if p.trabajador and p.trabajador.centro else '',
            p.fecha_inicio.strftime('%Y-%m-%d') if p.fecha_inicio else '',
            p.fecha_fin.strftime('%Y-%m-%d') if p.fecha_fin else '',
            p.justificacion or '',
            p.estado
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='permisos.csv'
    )
