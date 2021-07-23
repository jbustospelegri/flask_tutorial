from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

"""
    MODELO USUARIO
"""

# Esta clase representa a los usuarios de nuestra aplicación. Además, contiene la lógica para crear usuarios,
# guardar las contraseñas de modo seguro y verificarlas.

# Flask-login permite definir una clase para los usuarios. Esto hace posible que se pueda utilizar cualquier sistema
# de base de datos y que modifiquemos el modelo en función de las necesidades que vayan surgiendo. El único requisito
# indicado por flask-login es que la clase usuario debe implementar las siguientes propiedades y metodos:
#
#   - is_authenticated: True si el usuario está autenticado. False caso contrario
#   - is_active: True si la cuenta de usuario está activa (es decir, por ejemplo se ha verificado el email al registrarse)
#   - is_anonymous: True para usuarios anónimos y False para usuarios reales
#   - get_id(): devuelve un string con el ID del usuario. Es obligatorio que devuelva un string
#
#  La clase UserMixin ya contiene todas las propiedades mencionadas anteriormente


class User(db.Model, UserMixin):

    # Para poder gestionar los usuarios mediante db, la clase User debe de heredar la classe Model del objeto de
    # database definido

    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(128), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """
        Para guardar las contraseñas del usuario, se utilizará un hash del password mediante la librería
        werkzeug.security
        :param password:
        :return:
        """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Para poder verificar la contraseña, se debe de utilizar el hash juntamente con la contraseña
        :param password:
        :return:
        """
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f'<User {self.email}>'
