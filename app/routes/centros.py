# app/routes/centros.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app.models import Centro, Empresa, Trabajador, Horario
from app import db
from sqlalchemy.exc import IntegrityError  # ✅ nuevo

bp = Blueprint('centros', __name__, url_prefix='/centros')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def lista_centros():
    if current_user.rol not in ['admin', 'empresa']:
        flash(_('No tienes permiso para ver esta página.'), 'danger')
        return redirect(url_for('dashboard.index'))

    mostrar_inactivos = request.args.get('inactivos') == '1'
    empresa_filtro_id = request.args.get('empresa_filtro', type=int)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        empresa_id = request.form.get('empresa_id')
        if not nombre or not empresa_id:
            flash(_('Todos los campos son obligatorios.'), 'danger')
        else:
            nuevo = Centro(nombre=nombre, empresa_id=empresa_id)
            db.session.add(nuevo)
            db.session.commit()
            flash(_('Centro registrado correctamente.'), 'success')
            return redirect(url_for('centros.lista_centros'))

    query = Centro.query

    if current_user.rol != 'admin':
        query = query.filter_by(empresa_id=current_user.empresa_id)
    elif empresa_filtro_id:
        query = query.filter_by(empresa_id=empresa_filtro_id)

    if mostrar_inactivos:
        query = query.filter_by(activo=False)
    else:
        query = query.filter_by(activo=True)

    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    # Evitar errores con atributos inexistentes
    if sort == 'empresa':
        sort_attr = Empresa.nombre
        query = query.join(Empresa)
    else:
        sort_attr = getattr(Centro, sort, Centro.id)

    sort_attr = sort_attr.desc() if order == 'desc' else sort_attr.asc()

    centros = query.order_by(sort_attr).all()

    empresas = Empresa.query.order_by(Empresa.nombre).all() if current_user.rol == 'admin' else [current_user.empresa]

    return render_template('centros.html',
                           centros=centros,
                           empresas=empresas,
                           mostrar_inactivos=mostrar_inactivos,
                           empresa_filtro_id=empresa_filtro_id)


@bp.route('/borrar/<int:centro_id>', methods=['POST'])
@login_required
def borrar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    centro.activo = False
    db.session.commit()
    flash(_('Centro marcado como eliminado.'), 'warning')
    return redirect(url_for('centros.lista_centros', inactivos=1))


@bp.route('/restaurar/<int:centro_id>', methods=['POST'])
@login_required
def restaurar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    centro.activo = True
    db.session.commit()
    flash(_('Centro restaurado correctamente.'), 'success')
    return redirect(url_for('centros.lista_centros', inactivos=1))


@bp.route('/<int:centro_id>/plantilla')
@login_required
def ver_plantilla(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    trabajadores = Trabajador.query.filter_by(centro_id=centro.id, activo=True).all()

    return render_template('plantilla_centro.html', centro=centro, trabajadores=trabajadores)


@bp.route('/eliminar_definitivo/<int:centro_id>', methods=['POST'])
@login_required
def eliminar_definitivo(centro_id):
    centro = Centro.query.get_or_404(centro_id)

    if centro.activo:
        flash(_('No puedes eliminar definitivamente un centro activo.'), 'danger')
        return redirect(url_for('centros.lista_centros'))

    trabajadores = centro.trabajadores[:]
    for t in trabajadores:
        Horario.query.filter_by(trabajador_id=t.id).delete()
        t.centro_id = None

    db.session.delete(centro)
    db.session.commit()

    flash(_('Centro eliminado permanentemente y trabajadores desvinculados.'), 'success')
    return redirect(url_for('centros.lista_centros', inactivos=1))


@bp.route('/editar/<int:centro_id>', methods=['POST'])
@login_required
def editar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)

    centro.nombre = request.form.get('nombre')
    centro.empresa_id = request.form.get('empresa_id')

    # Campos opcionales del drawer
    centro.email = request.form.get('email') or None
    centro.telefono = request.form.get('telefono') or None
    centro.direccion = request.form.get('direccion') or None
    centro.codigo_postal = request.form.get('codigo_postal') or None
    centro.ccc = request.form.get('ccc') or None
    centro.cif = request.form.get('cif') or None
    centro.responsable = request.form.get('responsable') or None
    centro.sector = request.form.get('sector') or None

    try:
        db.session.commit()
        flash(_('Centro actualizado correctamente.'), 'success')
    except IntegrityError:
        db.session.rollback()
        flash(_('Error: ya existe otro centro con datos duplicados como CIF o CCC.'), 'danger')

    return redirect(url_for('centros.lista_centros'))
