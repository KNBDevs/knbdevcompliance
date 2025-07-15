# seed.py

from app import create_app, db
from app.models import User, Empresa, Trabajador
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crear todas las tablas si no existen
    db.create_all()

    # Crear admin si no existe
    if not User.query.filter_by(email='admin@controlhorario.com').first():
        admin = User(
            email='admin@controlhorario.com',
            nombre='Administrador',
            password=generate_password_hash('admin123'),
            rol='admin'
        )
        db.session.add(admin)
        print("✅ Usuario administrador creado.")

    # Crear empresa demo si no existe
    if not Empresa.query.first():
        empresa = Empresa(nombre='Empresa Demo')
        db.session.add(empresa)
        print("🏢 Empresa demo creada.")

    # Crear trabajador demo si no existe
    if not Trabajador.query.first():
        trabajador = Trabajador(
            nombre='Trabajador Demo',
            email='demo@empresa.com',
            telefono='000000000',
            dni='00000000A',
            centro_trabajo='Oficina Central',
            empresa_id=1  # Asegúrate que coincide con la creada arriba
        )
        db.session.add(trabajador)
        print("👷 Trabajador demo creado.")

    # Guardar cambios
    db.session.commit()
    print("✅ Base de datos inicializada correctamente.")
