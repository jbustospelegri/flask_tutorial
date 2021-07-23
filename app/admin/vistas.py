from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import Post
from . import admin_bp
from .forms import PostForm

# Para proteger una vista se utiliza el decorador @login_required
@login_required
@admin_bp.route('/admin/post/', methods=['GET', 'POST'], defaults={'post_id': None})
@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        # Cuando se hace uso de los blueprints, para realizar el redirect se debe de otorgar el nombre del blueprint
        # del que forma parte (el nombre se refiere al primer parámetro del blueprint).
        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", post_id=post_id, form=form)