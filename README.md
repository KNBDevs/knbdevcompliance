# 📋 APP REGISTRO CONTROL HORARIO

**Versión:** 1.0  
**Autor:** KNBDev  
**Licencia:** Propiedad exclusiva de José Francisco Nieto Barceló (KNBDev).
Todos los derechos reservados. No se permite la reproducción, distribución o uso comercial sin autorización expresa.  
**Lenguaje:** Python 3.10+ (Flask)  
**Base de datos:** SQLite (una instancia por cliente)

---

## 📌 Descripción general

Aplicación web extremadamente sencilla y funcional para el **control horario laboral**, pensada para funcionar en local o en red interna, sin necesidad de internet.  

Incluye:

- Panel de administración para empresas y trabajadores.
- Registro de fichajes (entrada/salida) desde una tablet Android.
- Gestión de vacaciones, permisos, horarios y centros.
- Exportación de datos en CSV.
- Compatible con varios idiomas.
- Interfaz adaptable y accesible.
- Funcionamiento **100% independiente por cliente**.

---

## 🧩 Estructura técnica del proyecto

```
KNBDEV_FICHAJE/
├── app/
│   ├── routes/
│   ├── forms.py
│   ├── models.py
│   └── __init__.py
├── static/
│   ├── css/
│   ├── img/
│   ├── js/
│   └── lang/
├── templates/
│   ├── partials/
│   └── *.html
├── migrations/
├── app.db
├── app.wsgi
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10 o superior
- SQLite (viene por defecto con Python)
- Hosting con soporte para aplicaciones Python (como Hostinguer con acceso SSH)

---

## 🧪 Uso en entorno local (desarrollo)

### 1. Crear entorno virtual

```powershell
# Si ya existe uno anterior
Remove-Item -Recurse -Force .\venv\

# Crear entorno
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente si no tienes el archivo `requirements.txt` actualizado:

```bash
pip install flask flask_sqlalchemy flask_login flask_babel flask_wtf email_validator flask_migrate
```

### 3. Crear usuario administrador (primer uso)

```bash
flask shell
```

```python
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

admin_user = User(
    nombre="Administrador",
    email="admin@controlhorario.com",
    password_hash=generate_password_hash("admin123"),
    rol="admin",
    empresa_id=None
)

db.session.add(admin_user)
db.session.commit()
print("Usuario administrador creado con éxito.")
```

### 4. Iniciar servidor

```bash
flask run
```

Accede a la aplicación desde:

```
http://localhost:5000/auth/login
```

### 🔐 Credenciales por defecto

```
Email:    admin@controlhorario.com  
Password: admin123
```

---

## 📤 Despliegue para un nuevo cliente (Hostinguer o VPS)

Cada cliente debe tener su propia instalación del sistema.

### 📁 Estructura recomendada:

```
clienteX/
├── app/
├── static/
├── templates/
├── app.wsgi
├── clienteX_app.db
├── config.py  # apuntando a 'sqlite:///clienteX_app.db'
├── requirements.txt
├── run.py
```

### 🧭 Pasos en Hostinguer:

1. Crear carpeta `controlhorario/` y subir el `.zip`
2. Descomprimir y crear app Python en el panel
3. Definir `app.wsgi` como punto de entrada
4. Entrar por SSH y ejecutar:

```bash
cd ~/controlhorario
source ../venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Seguridad por cliente

Cada cliente tiene su propia base de datos SQLite, por lo que los datos son completamente privados y no compartidos. La estructura soporta la instalación aislada por:

- Dominio (ej. `empresaXYZ.com`)
- Subdominio (ej. `control.empresaXYZ.com`)
- Carpeta en hosting

---

## 🌍 Traducciones

Archivos de idioma en:

```
static/lang/
```

Idiomas incluidos:
- Español (es)
- Inglés (en)
- Alemán, Francés, Italiano, Portugués, Árabe, Ruso, Chino, Japonés, etc.

---

## 📦 Preparación para entrega a cliente

1. Asegúrate de que:
   - `venv/`, `__pycache__/`, `.pyc` estén eliminados
   - `app.wsgi` esté presente
   - `config.py` apunte a una base de datos personalizada (`clienteX_app.db`)
2. Comprime el contenido en un `.zip` llamado por ejemplo:

```
CONTROL_HORARIO_EMPRESA_XYZ.zip
```

3. Entrega o despliega en el hosting asignado

---

## 💬 Contacto

Para soporte técnico, nuevas instalaciones o consultas comerciales:

📧 knb.dev.88@gmail.com  
🌐 https://knbdev.com