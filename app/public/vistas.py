from flask import render_template, abort

from app.models import Post
from . import public_bp

# Todas las funciones/metodos que contienen el decorador route (routing) son vistas
# de una página web (son un *endpoint*). Es decir, cuando se introduce la URL definida dentro de app.route, se
# ejecuta la función decorada.
@public_bp.route('/index')
@public_bp.route('/')
def index():
    # Los valores asignados a return deben de ser un objeto del tipo response o una tupla con los valores
    # (response, status, headers). Cuando se devuelve un string, este se devuelve con un response 200, el texto y un
    # text/html del tipo mime (Multi-purpose Internet Mail Extensions). Flask, convierte el valor que devuelve una vista
    # en un objeto response de forma automática.
    # return f'{len(posts)}'

    # Para renderizar una página web, Flask trae por defecto un motor renderizado de plantillas llamado Jinja2 que
    # permitirá crear páginas dinámicas en la aplicación web.
    # *Flask buscará las plantillas en el directorio templates* de nuestro proyecto. La carpeta se debe de situar en el
    # mismo nivel en el que se encuentre la aplicación (run.py en el ejemplo).

    # Por otra parte, para agregar los ficheros estáticos (su contenido no se modifica a lo largo del ciclo de ejecución
    # de la págína web. Estos ficherose estáticos permiten definir estilos, imagenes y código JS y deberemos
    # de contenerlos en un *directorio llamado static que será accesible mediante la URL /static*.

    # Para renderizar las plantillas se debe utilizar el método *render_template()*. Los parámetros introducidos
    # en render template serán interpretados por jinja como variables que podrán ser manipulados mediante {{ var }}.
    # Adicionalmente, para poder utilizar sentencias python renderizadas mediante jinja, se deberán de utilizar los
    # carácteres {% %}.

    # Por defecto Jinja2 escapa a cualquier carácter específico del lenguaje HTML al renderizar una plantilla, por lo
    # que si un método devuelve un string en formto <p> </p> se sustituirían los corchetes por &gt y &lt

    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)

# Las URLs pueden ser variables y dinámicas en función de como el usuario vaya navegando por la web. En este sentido,
# no se podría crear una vista para cada URL creada y el objetivo debería de ser crear una URL única parametrizada
# que englobase vistas que compartan un mismo objetivo. Para ello, la url se parametriza mediante variables englobadas
# como <converter: param>. El converter indica el tipo de datos que contiene el parametro. Existen distintos tipos de
# concersores.
#   - string
#   - int/float
#   - path (acepta cadenas que contienen /)
#   - uuid (acepta cadenas que contienen un formato uuid)
# Adicionalmente, se pueden crear conversores própios.
@public_bp.route('/p/<string:slug>/', methods=['POST'])
def show_post(slug):
    # El método url_for() permite crear una URL a partir del nombre de un metodo que actua como vista.
    # Esta función acepta como parámetros de entrada las variables del metodo y un número variable de argumentos
    # clave valor. Si los argumentos clave valor se encuentran fuera de las variables de entrada de la vista,
    # se indicarán con ?.
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template('public/post_view.html', post=post)