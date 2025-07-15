# app/routes/dashboard.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Empresa, Centro, Trabajador, Fichaje, User, Horario
from flask_babel import gettext as _
from datetime import date, datetime, timedelta
from sqlalchemy import func, extract
from collections import defaultdict

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    datos = {}

    hoy = date.today()

    if current_user.rol == 'admin':
        datos['empresas'] = Empresa.query.count()
        datos['centros'] = Centro.query.count()
        datos['trabajadores'] = Trabajador.query.count()
        datos['usuarios'] = User.query.count()

        # Fichajes de hoy
        datos['fichajes_hoy'] = Fichaje.query.filter(Fichaje.fecha == hoy).count()

        # Pendientes: trabajadores sin fichaje hoy
        trabajadores_hoy = Trabajador.query.all()
        trabajadores_con_fichaje = (
            Fichaje.query.filter(Fichaje.fecha == hoy)
            .with_entities(Fichaje.trabajador_id)
            .distinct()
            .all()
        )
        fichadores_ids = {f.trabajador_id for f in trabajadores_con_fichaje}
        datos['pendientes_hoy'] = len([t for t in trabajadores_hoy if t.id not in fichadores_ids])

        # Top puntualidad semanal (simplificado: entrada antes de las 9:00)
        semana = date.today().isocalendar()[1]
        fichajes = Fichaje.query \
            .filter(extract('week', Fichaje.fecha) == semana) \
            .filter(Fichaje.hora <= datetime.strptime("09:00", "%H:%M").time()) \
            .with_entities(Fichaje.trabajador_id, func.count().label('puntual')) \
            .group_by(Fichaje.trabajador_id) \
            .order_by(func.count().desc()) \
            .limit(3).all()

        datos['top_puntualidad'] = []
        for f in fichajes:
            trabajador = Trabajador.query.get(f.trabajador_id)
            datos['top_puntualidad'].append({'nombre': trabajador.nombre, 'minutos_antes': f.puntual})

        # Incidencias ficticias: trabajadores sin horario
        datos['sin_horario'] = Trabajador.query.filter(~Trabajador.horarios.any()).all()

        # Gráfico de fichajes últimos 7 días
        dias = [(hoy - timedelta(days=i)) for i in range(6, -1, -1)]
        fichajes_por_dia = defaultdict(int)

        resultados = (
            Fichaje.query
            .with_entities(Fichaje.fecha, func.count().label('total'))
            .filter(Fichaje.fecha.in_(dias))
            .group_by(Fichaje.fecha)
            .all()
        )

        for r in resultados:
            fichajes_por_dia[r.fecha] = r.total

        datos['grafico_fechas'] = [d.strftime('%d/%m') for d in dias]
        datos['grafico_valores'] = [fichajes_por_dia.get(d, 0) for d in dias]

    elif current_user.rol == 'trabajador':
        datos['fichajes_recientes'] = current_user.fichajes[-5:]  # opcional

    return render_template('dashboard.html', datos=datos)
