# app/models.py

from datetime import datetime
from app import db
from flask_login import UserMixin

# Asociación entre responsables y centros
responsables_centros = db.Table('responsables_centros',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('centro_id', db.Integer, db.ForeignKey('centro.id'))
)

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    cif = db.Column(db.String(20), unique=True, nullable=False)
    ccc = db.Column(db.String(20), unique=True, nullable=False)
    contacto = db.Column(db.String(100))
    administrador = db.Column(db.String(100))  
    telefono = db.Column(db.String(30))        
    email = db.Column(db.String(120))          
    sede_fiscal = db.Column(db.String(255))    
    codigo_postal = db.Column(db.String(10))   
    iban = db.Column(db.String(34))            
    activo = db.Column(db.Boolean, default=True)

    centros = db.relationship('Centro', back_populates='empresa', cascade="all, delete")


class TrabajadorCurso(db.Model):
    __tablename__ = 'trabajador_cursos'
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajador.id'), primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), primary_key=True)
    fecha_asignacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    trabajador = db.relationship('Trabajador', back_populates='cursos_asociados')
    curso = db.relationship('Curso', back_populates='trabajadores_asociados')


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)  # NUEVO CAMPO
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    icono = db.Column(db.String(10))  # Emoji o clase CSS
    color = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    trabajadores_asociados = db.relationship('TrabajadorCurso', back_populates='curso', cascade="all, delete-orphan")


class Trabajador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    dni = db.Column(db.String(20), nullable=False)
    pin = db.Column(db.String(5), nullable=False)
    centro_id = db.Column(db.Integer, db.ForeignKey('centro.id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    rol = db.Column(db.String(20), default='trabajador')
    nass = db.Column(db.String(20))
    nacionalidad = db.Column(db.String(60))
    genero = db.Column(db.String(10))
    iban = db.Column(db.String(34))
    cursos_asociados = db.relationship('TrabajadorCurso', back_populates='trabajador', cascade="all, delete-orphan")



    centro = db.relationship(
        'Centro',
        backref=db.backref('trabajadores', lazy='joined'),
        lazy='joined'
    )

    fichajes = db.relationship(
        'Fichaje',
        backref='trabajador',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    vacaciones = db.relationship(
        'Vacacion',
        backref='trabajador',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    horarios = db.relationship(
        'Horario',
        backref='trabajador',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Centro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    email = db.Column(db.String(120))
    telefono = db.Column(db.String(30))
    direccion = db.Column(db.String(255))
    codigo_postal = db.Column(db.String(10))
    ccc = db.Column(db.String(50))
    cif = db.Column(db.String(50))
    responsable = db.Column(db.String(120))
    sector = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship('Empresa', back_populates='centros')


class User(UserMixin, db.Model):  # Administradores, responsables, etc.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'admin', 'empresa', 'centro'
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))  # si aplica

    centros = db.relationship(
        'Centro',
        secondary=responsables_centros,
        backref=db.backref('responsables', lazy='dynamic')
    )

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(
        db.Integer,
        db.ForeignKey('trabajador.id', ondelete='CASCADE'),
        nullable=False
    )
    dia_semana = db.Column(db.String(10), nullable=False)
    hora_entrada = db.Column(db.Time, nullable=True)
    hora_salida = db.Column(db.Time, nullable=True)

class Fichaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    hora = db.Column(db.Time, default=datetime.utcnow)
    tipo = db.Column(db.String(10))
    trabajador_id = db.Column(
        db.Integer,
        db.ForeignKey('trabajador.id', ondelete='CASCADE'),
        nullable=False
    )

class Vacacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    justificacion = db.Column(db.String(255))
    estado = db.Column(db.String(20), default='pendiente')
    trabajador_id = db.Column(
        db.Integer,
        db.ForeignKey('trabajador.id', ondelete='CASCADE'),
        nullable=False
    )


class ReconocimientoMedico(db.Model):
    __tablename__ = 'reconocimiento_medico'

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(
        db.Integer,
        db.ForeignKey('trabajador.id', ondelete='CASCADE'),
        nullable=False
    )
    fecha = db.Column(db.Date, nullable=False)
    observaciones = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    trabajador = db.relationship('Trabajador', backref=db.backref('reconocimientos', lazy=True, cascade='all, delete-orphan'))
