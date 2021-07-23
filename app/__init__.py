"""
    En la inicialización del paquete de la app hay que registrar todos los Blueprints.
    Este fichero contiene métodos factoría para crear e inicializar la app y los distintos componentes y extensiones.
"""
import urllib

from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

driver = 'ODBC Driver 17 for SQL Server'
server = 'DESKTOP-77UPMNB\SQLEXPRESS'
db_name = 'miniblog'
params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={db_name};trusted_connection=yes")

# La clase Login Manager debe ser accesible desde cualquier punto de nuestra aplicación. Esta clase permite cargar un
# usuario a partir del ID guardado en la sesión o redirigir los usuarios que no están autenticados a la página de login
# cuando intentan acceder a una vista protegida. Como Flask Login hace uso de la sesión para la autenticación, debemos
# establecer la variable SECRET_KEY.
login_manager = LoginManager()

# Para poder gestionar flask con una base de datos se debe de crear un objeto de base de datos. Lo bueno de utilizar una
# base de datos es que los datos son persistentes y perduran incluso tras reiniciar el servidor
db = SQLAlchemy()


# En este módulo se define un método factoría para crear la app, inicializar las diferentes extensiones y registrar los
# blueprints. A diferencia de cómo lo hacíamos hasta ahora, los métodos factoría nos permiten configurar diferentes apps
# a partir del mismo proyecto inicializando diferentes extensiones y registrando distintos Blueprints.
def create_app():
    # Toda aplicación Flask es una instancia WSGI (Web Server Gategay Instance) de la clase Flask. El argumento que
    # recibe dicho objeto de la clase es el nombre del modulo de la aplicación. Esto es necesario para que flask sepa
    # donde encontrar las plantillas o los ficheros estáticos.
    app = Flask(__name__)


    # *Para poder lanzar la aplicación haciendo uso del servidor interno de flask (local host puerto 5000) se debe de *
    # *declarar la variable FLASK_APP en el fichero venv/bin/activate.bat o venv/scripts/activate.bat*
    # *Para poder hacer debugs, se deve de setear la variable FLASK_ENV=development en el fichero activate.bat*

    # Clave secreta para poder evitar los ataques CSRF en Flask. Esta clave no debe saberse
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    # Se debe de configurar la connexión a sql configurando SQLALCHEMY_DATABASE_URI dentro del diccionario de
    # configuración de flask
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={params}'

    # Se debe de configurar el parámetro SQLALCHEMY_TRACK_MODIFICATIONS como False para evitar que se envíe una señal
    # cada vez que se modifica un objeto
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)

    # Si queremos que un usuario no reciba un mensaje de error 401 cuando intente acceder a una vista protegida, se debe
    # de indicar al objeto login_manager cuál es la vista para realizar el login
    login_manager.login_view = 'auth.login'

    db.init_app(app)

    # Registro de los blueprints
    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    return app









