from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Trabajador, Horario
from app import db
from flask_babel import gettext as _
from datetime import time

bp = Blueprint('horarios', __name__, url_prefix='/horarios')

DIAS_SEMANA = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

# NUEVA VISTA: Lista general de trabajadores para acceder a sus horarios
@bp.route('/')
@login_required
def lista_horarios():
   
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')

    query = Trabajador.query

    if sort == 'email':
        column = Trabajador.email
    elif sort == 'telefono':
        column = Trabajador.telefono
    elif sort == 'centro':
        column = Trabajador.centro_id
    elif sort == 'nombre':
        column = Trabajador.nombre
    else:
        column = Trabajador.nombre  # fallback seguro

    if sort:
        if order == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
    else:
        query = query.order_by(Trabajador.nombre.asc())  # sin sort → orden natural sin icono

    trabajadores = query.all()
    return render_template('lista_horarios.html', trabajadores=trabajadores)



# VISTA EXISTENTE: Editar horarios de un trabajador concreto
@bp.route('/<int:trabajador_id>', methods=['GET', 'POST'])
@login_required
def gestionar_horario(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)

    # TODO: Comprobación de permisos según el rol

    if request.method == 'POST':
        for dia in DIAS_SEMANA:
            entrada = request.form.get(f"{dia}_entrada")
            salida = request.form.get(f"{dia}_salida")

            # Convertir a objeto time
            try:
                hora_entrada = time.fromisoformat(entrada) if entrada else None
                hora_salida = time.fromisoformat(salida) if salida else None
            except ValueError:
                flash(_(f"Formato inválido para {dia}."), 'danger')
                return redirect(request.url)

            # Buscar horario existente
            horario = Horario.query.filter_by(trabajador_id=trabajador.id, dia_semana=dia).first()

            if horario:
                horario.hora_entrada = hora_entrada
                horario.hora_salida = hora_salida
            else:
                nuevo = Horario(
                    trabajador_id=trabajador.id,
                    dia_semana=dia,
                    hora_entrada=hora_entrada,
                    hora_salida=hora_salida
                )
                db.session.add(nuevo)

        db.session.commit()
        flash(_('Horario actualizado correctamente.'), 'success')
        return redirect(url_for('horarios.gestionar_horario', trabajador_id=trabajador.id))

    # GET: obtener horarios existentes
    horarios = {h.dia_semana: h for h in trabajador.horarios}
    return render_template('horarios.html', trabajador=trabajador, dias=DIAS_SEMANA, horarios=horarios)
