# app/routes/empresas.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.models import Empresa
from app import db
from flask_babel import gettext as _

bp = Blueprint('empresas', __name__, url_prefix='/empresas')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def lista_empresas():
    if current_user.rol != 'admin':
        flash(_('No tienes permiso para ver esta página.'), 'danger')
        return redirect(url_for('dashboard.index'))

    mostrar_inactivas = request.args.get('inactivas') == '1'

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cif = request.form.get('cif')
        ccc = request.form.get('ccc')

        if not nombre or not cif or not ccc:
            flash(_('Todos los campos son obligatorios.'), 'danger')
        else:
            # Validación previa para evitar duplicados
            empresa_existente = Empresa.query.filter(
                (Empresa.cif == cif) | (Empresa.ccc == ccc)
            ).first()

            if empresa_existente:
                flash(_('Ya existe una empresa con ese CIF o CCC.'), 'danger')
            else:
                nueva = Empresa(nombre=nombre, cif=cif, ccc=ccc)
                db.session.add(nueva)
                try:
                    db.session.commit()
                    flash(_('Empresa registrada con éxito.'), 'success')
                    return redirect(url_for('empresas.lista_empresas'))
                except IntegrityError:
                    db.session.rollback()
                    flash(_('Error al registrar la empresa. Verifica que el CIF y CCC no estén duplicados.'), 'danger')

    query = Empresa.query
    if not mostrar_inactivas:
        query = query.filter_by(activo=True)
    else:
        query = query.filter_by(activo=False)

    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    sort_attr = getattr(Empresa, sort, Empresa.id)
    if order == 'desc':
        sort_attr = sort_attr.desc()
    else:
        sort_attr = sort_attr.asc()

    empresas = query.order_by(sort_attr).all()

    return render_template('empresas.html', empresas=empresas, mostrar_inactivas=mostrar_inactivas)

@bp.route('/borrar/<int:empresa_id>', methods=['POST'])
@login_required
def borrar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)

    empresa.activo = False
    for centro in empresa.centros:
        centro.activo = False
        for trabajador in centro.trabajadores:
            trabajador.activo = False

    db.session.commit()
    flash(_('Empresa y sus dependencias marcadas como inactivas.'), 'warning')
    inactivas = int(request.args.get('inactivas') == '1')
    return redirect(url_for('empresas.lista_empresas', inactivas=inactivas))

@bp.route('/restaurar/<int:empresa_id>', methods=['POST'])
@login_required
def restaurar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    empresa.activo = True

    for centro in empresa.centros:
        centro.activo = True
        for trabajador in centro.trabajadores:
            trabajador.activo = True

    db.session.commit()
    flash(_('Empresa y sus dependencias restauradas.'), 'success')
    inactivas = int(request.args.get('inactivas') == '1')
    return redirect(url_for('empresas.lista_empresas', inactivas=inactivas))

@bp.route('/eliminar_definitivo/<int:empresa_id>', methods=['POST'])
@login_required
def eliminar_definitiva_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)

    if empresa.activo:
        flash(_('No se puede eliminar una empresa activa.'), 'danger')
        return redirect(url_for('empresas.lista_empresas'))

    for centro in empresa.centros:
        for trabajador in centro.trabajadores:
            db.session.delete(trabajador)
        db.session.delete(centro)

    db.session.delete(empresa)
    db.session.commit()
    flash(_('Empresa y toda su estructura eliminadas permanentemente.'), 'success')
    inactivas = int(request.args.get('inactivas') == '1')
    return redirect(url_for('empresas.lista_empresas', inactivas=inactivas))

@bp.route('/editar/<int:empresa_id>', methods=['POST'])
@login_required
def editar_empresa(empresa_id):
    print(request.form)  # 👈 esto

    empresa = Empresa.query.get_or_404(empresa_id)
    empresa.nombre = request.form.get('nombre')
    empresa.cif = request.form.get('cif')
    empresa.ccc = request.form.get('ccc')
    empresa.contacto = request.form.get('contacto') or None

    # Nuevos campos
    empresa.administrador = request.form.get('administrador') or None
    empresa.telefono = request.form.get('telefono') or None
    empresa.email = request.form.get('email') or None
    empresa.sede_fiscal = request.form.get('sede_fiscal') or None
    empresa.codigo_postal = request.form.get('codigo_postal') or None
    empresa.iban = request.form.get('iban') or None

    db.session.commit()
    flash(_('Empresa actualizada correctamente.'), 'success')
    return redirect(url_for('empresas.lista_empresas'))
