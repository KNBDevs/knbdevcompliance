# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_migrate import Migrate
from config import Config

import os

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
migrate = Migrate()

def create_app():
    # Definir rutas absolutas para templates y static fuera de app/
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    # Asegurar que /data existe (Render permite escribir ahí)
    os.makedirs('/data', exist_ok=True)

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)
    
    print("📁 Usando base de datos:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    from app.routes.fichaje_trabajador import bp as fichaje_bp


    # Configuración de login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Registrar blueprints principales
    from app.routes import auth, dashboard, empresas, centros, trabajadores, fichajes, permisos, exportar, horarios
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(empresas.bp)
    app.register_blueprint(centros.bp)
    app.register_blueprint(trabajadores.bp)
    app.register_blueprint(fichajes.bp)
    app.register_blueprint(permisos.bp)
    app.register_blueprint(exportar.bp)
    app.register_blueprint(horarios.bp)
    app.register_blueprint(fichaje_bp)


    # ✅ Registrar blueprint de prevención
    from app.routes.prevencion import bp_prevencion
    app.register_blueprint(bp_prevencion)

    # ✅ Registrar blueprint de reconocimientos médicos
    from app.routes.reconocimientos import bp_reconocimientos
    app.register_blueprint(bp_reconocimientos)

    # Cargar usuario para Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ Activar claves foráneas en SQLite
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    import sqlite3

    @event.listens_for(Engine, "connect")
    def activar_foreign_keys_sqlite(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return app
