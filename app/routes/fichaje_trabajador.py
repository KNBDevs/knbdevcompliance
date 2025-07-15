# app/routes/fichaje_trabajador.py

from flask import Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime, timedelta
from urllib.parse import quote
import random

bp = Blueprint('fichaje', __name__, url_prefix='/fichaje')


@bp.route('/')
def login():
    return render_template('login.html')


@bp.route('/dashboard')
def dashboard():
    from app.models import Trabajador

    trabajador_id = session.get('trabajador_id')
    if not trabajador_id:
        return redirect(url_for('fichaje.login'))

    trabajador = Trabajador.query.get(trabajador_id)
    now = datetime.now()
    return render_template('dashboard_trabajador.html', trabajador=trabajador, now=now)


@bp.route('/fichar', methods=['POST'])
def fichar():
    from app import db
    from app.models import Fichaje, Trabajador, Horario

    dni5 = request.form.get('dni5')
    if not dni5:
        return redirect(url_for('auth.login', fichaje='error'))

    trabajador = Trabajador.query.filter_by(
        pin=dni5,
        activo=True
    ).first()


    if not trabajador:
        return redirect(url_for('auth.login', fichaje='error'))

    hoy = datetime.today().date()
    ahora = datetime.now().replace(second=0, microsecond=0)

    # Día de la semana en español
    dias_es = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    dia_actual = dias_es[ahora.weekday()]

    # Buscar horario del trabajador para hoy
    horario = Horario.query.filter_by(
        trabajador_id=trabajador.id,
        dia_semana=dia_actual
    ).first()

    def tiene_horario_asignado(h):
        return bool(h and h.hora_entrada and h.hora_salida)

    tiene_horario = tiene_horario_asignado(horario)

    def hora_random(base_dt):
        return (base_dt + timedelta(minutes=random.randint(-10, 10))).time()

    def generar_horas_entrada_salida(hora_entrada_dt, hora_salida_dt):
        for _ in range(10):
            h_entrada = hora_random(hora_entrada_dt)
            h_salida = hora_random(hora_salida_dt)
            if h_entrada < h_salida:
                return h_entrada, h_salida
        return hora_entrada_dt.time(), hora_salida_dt.time()

    fichajes_hoy = Fichaje.query.filter_by(
        trabajador_id=trabajador.id,
        fecha=hoy
    ).order_by(Fichaje.hora).all()

    if tiene_horario:
        hora_entrada_dt = datetime.combine(hoy, horario.hora_entrada)
        hora_salida_dt = datetime.combine(hoy, horario.hora_salida)
        margen_entrada_inicio = hora_entrada_dt - timedelta(minutes=10)
        margen_salida_fin = hora_salida_dt + timedelta(minutes=10)

        print("🕒 ahora:", ahora)
        print("⏰ margen_entrada_inicio:", margen_entrada_inicio)
        print("⏰ margen_salida_fin:", margen_salida_fin)

        if ahora < margen_entrada_inicio:
            print("❌ Demasiado pronto para fichar")
            return redirect(url_for(
                'auth.login',
                fichaje='demasiado_pronto',
                nombre=quote(trabajador.nombre)
            ))

        elif ahora > margen_salida_fin:
            print("❌ Demasiado tarde para fichar")
            return redirect(url_for(
                'auth.login',
                fichaje='demasiado_tarde',
                nombre=quote(trabajador.nombre)
            ))

        if fichajes_hoy:
            return redirect(url_for(
                'auth.login',
                fichaje='ya_fichado',
                nombre=quote(trabajador.nombre)
            ))

        hora_entrada, hora_salida = generar_horas_entrada_salida(hora_entrada_dt, hora_salida_dt)

        entrada = Fichaje(
            trabajador_id=trabajador.id,
            fecha=hoy,
            hora=hora_entrada,
            tipo='entrada'
        )
        salida = Fichaje(
            trabajador_id=trabajador.id,
            fecha=hoy,
            hora=hora_salida,
            tipo='salida'
        )

        db.session.add_all([entrada, salida])
        db.session.commit()

        return redirect(url_for(
            'auth.login',
            fichaje='ok',
            nombre=quote(trabajador.nombre),
            hora=entrada.hora.strftime('%H:%M'),
            entrada=horario.hora_entrada.strftime('%H:%M'),
            salida=horario.hora_salida.strftime('%H:%M'),
            tipo='entrada'
        ))

    else:
        entradas = [f for f in fichajes_hoy if f.tipo == 'entrada']
        salidas = [f for f in fichajes_hoy if f.tipo == 'salida']

        if len(entradas) >= 2 and len(salidas) >= 2:
            return redirect(url_for(
                'auth.login',
                fichaje='limite_turnos',
                nombre=quote(trabajador.nombre)
            ))

        tipo = 'entrada'
        if not fichajes_hoy:
            turno_msg = ''
        elif fichajes_hoy[-1].tipo == 'entrada':
            if len(salidas) >= 2:
                return redirect(url_for(
                    'auth.login',
                    fichaje='limite_turnos',
                    nombre=quote(trabajador.nombre)
                ))
            tipo = 'salida'
            turno_msg = ''
        else:
            if len(entradas) >= 2:
                return redirect(url_for(
                    'auth.login',
                    fichaje='limite_turnos',
                    nombre=quote(trabajador.nombre)
                ))
            tipo = 'entrada'
            if len(entradas) == 1 and len(salidas) == 1:
                turno_msg = 'segundo_turno'
            else:
                turno_msg = ''

        nuevo_fichaje = Fichaje(
            trabajador_id=trabajador.id,
            fecha=hoy,
            hora=hora_random(ahora),
            tipo=tipo
        )

        db.session.add(nuevo_fichaje)
        db.session.commit()

        return redirect(url_for(
            'auth.login',
            fichaje='ok' if not turno_msg else turno_msg,
            nombre=quote(trabajador.nombre),
            hora=nuevo_fichaje.hora.strftime('%H:%M'),
            entrada='',
            salida='',
            tipo=tipo
        ))
