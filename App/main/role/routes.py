from flask import request, render_template, url_for
from werkzeug.utils import redirect
from App.main import main_blueprint
from App.models import Role
from App.user.routes import is_login


@main_blueprint.route('/roles/', methods=['GET', 'POST'])
@is_login
def roles_list():
    """角色信息列表"""
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('main/role/roles.html', roles=roles)


@main_blueprint.route('/addroles/', methods=['GET', 'POST'])
@is_login
def add_roles():
    """添加角色"""
    if request.method == 'GET':
        return render_template('addroles.html')
    if request.method == 'POST':

        r_name = request.form.get('r_name')
        role = Role(r_name=r_name)
        role.save()

        return redirect(url_for('main/role/addroles.html'))