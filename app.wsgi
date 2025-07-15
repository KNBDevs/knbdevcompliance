import sys
import os

# Asegúrate de que se incluye el directorio del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

application = create_app()  # Hostinguer espera esta variable exacta
