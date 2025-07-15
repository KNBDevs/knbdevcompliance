# app/routes/prevencion.py

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from datetime import datetime
from app.models import Trabajador, Centro, Curso, TrabajadorCurso, db

bp_prevencion = Blueprint('prevencion', __name__, url_prefix='/prevencion')


@bp_prevencion.route('/')
@login_required
def panel_prevencion():
    return render_template('prevencion.html')


@bp_prevencion.route('/formacion')
@login_required
def formacion():
    centros = Centro.query.filter_by(activo=True).all()
    trabajadores = Trabajador.query.filter_by(activo=True).all()
    return render_template('formacion.html', centros=centros, trabajadores=trabajadores)


# ✅ Obtener cursos + asignados
@bp_prevencion.route('/cursos/<int:trabajador_id>', methods=['GET'])
@login_required
def obtener_cursos_trabajador(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)
    cursos_todos = Curso.query.filter_by(activo=True).all()

    # Extraer los IDs de los cursos asignados
    cursos_asignados = [tc.curso_id for tc in trabajador.cursos_asociados]

    return jsonify({
        "todos": [
            {"id": c.id, "nombre": c.nombre, "icono": c.icono or ""} for c in cursos_todos
        ],
        "asignados": cursos_asignados
    })


# ✅ Guardar cursos (con fecha)
@bp_prevencion.route('/cursos/<int:trabajador_id>', methods=['POST'])
@login_required
def guardar_cursos_trabajador(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)
    data = request.get_json()
    nuevos_ids = set(data.get("cursos", []))

    # Mapa de cursos ya asignados
    asignaciones_actuales = {tc.curso_id: tc for tc in trabajador.cursos_asociados}

    # Eliminar cursos desmarcados
    for curso_id in list(asignaciones_actuales.keys()):
        if curso_id not in nuevos_ids:
            db.session.delete(asignaciones_actuales[curso_id])

    # Añadir o actualizar cursos seleccionados
    for curso_id in nuevos_ids:
        if curso_id in asignaciones_actuales:
            # Ya asignado, actualizar fecha a ahora
            asignaciones_actuales[curso_id].fecha_asignacion = datetime.utcnow()
        else:
            # Nuevo curso
            nueva_asignacion = TrabajadorCurso(
                trabajador_id=trabajador.id,
                curso_id=curso_id,
                fecha_asignacion=datetime.utcnow()
            )
            db.session.add(nueva_asignacion)

    db.session.commit()
    return jsonify({"mensaje": "Cursos actualizados correctamente"})


@bp_prevencion.route('/reconocimientos')
@login_required
def reconocimientos():
    trabajadores = Trabajador.query.all()
    centros = Centro.query.all()
    return render_template('reconocimientos.html', trabajadores=trabajadores, centros=centros)
