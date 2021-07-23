"""
    Para poder organizar el código en un conjunto de modulos que sigan una división estructural o funcional es necesario
    utilizar un conjunto de componentes/modulos llamados Blueprints.

    Un Blueprint define una colección de vistas, plantillas, recursos estáticos, modelos, etc que pueden ser utilizados
    por la aplicación en diferentes módulos.

    Para usar un BluePrint siempre se seguirán los siguientes pasos:
        1- Creción e inicialización del Blueprint
        2- Registro del Blueprint en la app
"""

from flask import Blueprint

# Para crear un blueprint se deben inicializar 4 parámetros: un nombre; el nombre de la importación (nombre del módulo,
# normalmente representado por __name__, el nombre de los directorios para las plantillas y los recursos estáticos.
public_bp = Blueprint('public', __name__, template_folder='templates', static_folder='static')

# Además, es necesario importar todas las vistas del Blueprint para que la app sea consciente de que existen
from . import vistas

