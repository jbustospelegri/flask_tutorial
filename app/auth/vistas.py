from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for, render_template, request
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User


# La librería flask login permite implementar el login de usuarios en Flask. Esta librería permite
#   - Almacenar el ID del usuario en la sesión y mecanismos para hacer login y logout
#   - Restringir el acceso a ciertas vistas únicamente a los usuarios autenticados
#   - Gestionar la funcionalidad 'recuerdame' para mantener la sesión incluso después de que el usuario cierre el
#     navegador
#   - Proteger el acceso a las cookies de sesion frente a terceros

# Formularios:
# Un formulario sirve para que un usuario pueda interactuar con la aplicación web enviando cualquier tipo de información
# al servidor (aplicación Flask). Este envió de información se definen un conjunto de métodos de petición (verbos HTTP).
# Los más conocidos son:
#   - GET: sirve para recibir datos y no modificarlos.
#   - POST: envia un objeto a un recurso específico para que sean procesados.
#
# Para que Flask responda ante posts del usuario (interacción con la web) se deberá de añadir dicho parámetro al parámetro
# methods.
@auth_bp.route('/signup/', methods={'GET', 'POST'})
def show_signup_form():
    # Para obtener la información que el usuario introduce a través de la página web, se debe de utilizar el objeto request
    # de flask. Este, contiene las cabeceras HTTP, codificación, y los datos.

    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    # Para validar que el usuario añade correctamente los datos en el formulario (email correcto o introduce el
    # nombre) se debe *hacer uso de la extensión de flask Flas-WTF* basada en WTForms.
    form = SignupForm()

    error = None

    # El método validate_on_submit valida que los campos del form estén correctos.
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Se comprueba que no hay un usuario con ese email
        user = User.get_by_email(email)

        if user is not None:
            error = f'El email {email} ya esta siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            # Dejamos al usuario logueado
            login_user(user, remember=True)

            next = request.args.get('next', None)
            if next:
                return redirect(next)

            # Si el formulario se procesa adecuadamente, es una buena práctica hacer un redirect para evitar envíos duplicados
            # de datos (por ejemplo si el usuario recarga la pagina o hace clic en el botón de atrás del navegador).
            return redirect(url_for('public.index'))
    return render_template('auth/signup_form.html', formulario_html=form, error=error)

# Método para comprobar si las credenciales del usuario son válidas o no y que permite logear a un usuario.
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Primero, se comprueba si el usuario actual ya esta autenticado. Para ello se utiliza la instancia current_user de
    # Flask-Login. El valor de current_user será un objeto usuario si está autenticado (el que se obtiene mediante el
    # callback user_loader. Por defecto, si el usuario no esta autenticado es anónimo y se redirige a la página de
    # auteticación
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    # Se crea el formulario para que el usuario se registre
    form = LoginForm()

    # En caso de que el usuario pulse al botón de registrar (haga un post) se comprueba que los datos son correctos (ha
    # llenado el formulario de forma guay).
    if form.validate_on_submit():

        # Se recupera el mail con el que se ha logeado el usuario
        user = User.get_by_email(form.email.data)

        # Si el mail existe en la base de datos y la contraseña es correcta, se realiza el login del usuario. En caso
        # contrario, se redirige de nuevo a la pagina para realizar el registro.
        if user is not None and user.check_password(form.password.data):

            # En caso de que el mail y contraseña existan, se autentifica el usuario mediante login_user.
            login_user(user, remember=form.remember_me.data)

            # Se comprueba si se devuelve en la request el parámetro next. Esto sucederá cuando el usuario ha intentado
            # acceder a una página protegida pero no estaba autenticado. Por temas de seguridad, solo se tiene en cuenta
            # este parámetro si la ruta es relativa. De este modo, se evita redirigir a un usuario a un sitio fuera del
            # dominio.
            next_page = request.args.get('next')

            # Si no se recive el parámetro next o este no contiene una ruta relativa, redigiremos al usuario a la página
            # de inicio
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)

# Por otra parte, se debe de permitir a los usuario poder realizar el logout
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

# El decorador login_manager.user_loader permite recuperar el id del usuario que se encuentra en la sesión de forma que
# nos devuelva el objeto User.
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
