from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models import Trabajador, Centro, ReconocimientoMedico, db
from datetime import datetime

bp_reconocimientos = Blueprint('reconocimientos', __name__, url_prefix='/reconocimientos')

@bp_reconocimientos.route('/')
@login_required
def vista_general():
    centros = Centro.query.filter_by(activo=True).all()
    trabajadores = Trabajador.query.filter_by(activo=True).all()
    return render_template('reconocimientos.html', centros=centros, trabajadores=trabajadores)

@bp_reconocimientos.route('/<int:trabajador_id>', methods=['POST'])
@login_required
def guardar_reconocimiento(trabajador_id):
    data = request.get_json()
    fecha = datetime.strptime(data.get('fecha'), '%Y-%m-%d')
    observaciones = data.get('observaciones', '')

    nuevo = ReconocimientoMedico(
        trabajador_id=trabajador_id,
        fecha=fecha,
        observaciones=observaciones
    )
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"mensaje": "Reconocimiento guardado correctamente"})


@bp_reconocimientos.route('/trabajador/<int:trabajador_id>')
@login_required
def reconocimientos_individual(trabajador_id):
    trabajador = Trabajador.query.get_or_404(trabajador_id)
    reconocimientos = ReconocimientoMedico.query.filter_by(trabajador_id=trabajador.id).order_by(ReconocimientoMedico.fecha.desc()).all()
    return render_template('reconocimientos_individual.html', trabajador=trabajador, reconocimientos=reconocimientos)
