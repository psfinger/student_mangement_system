from flask import request, render_template, url_for
from werkzeug.utils import redirect
from App.main import main_blueprint
from App.models import Role, Permission, RP
from App.user.routes import is_login


@main_blueprint.route('/roles/', methods=['GET', 'POST'])
@is_login
def roles_list():
    """角色信息列表"""
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = int(request.args.get('page_num', 5))
        paginate = Role.query.order_by('r_id').paginate(page, page_num)
        roles = paginate.items
        return render_template('main/role/roles.html', roles=roles, paginate=paginate)


@main_blueprint.route('/addroles/', methods=['GET', 'POST'])
@is_login
def add_roles():
    """添加角色"""
    if request.method == 'GET':
        return render_template('main/role/addroles.html')
    if request.method == 'POST':
        r_name = request.form.get('r_name')
        if not r_name:
            message = "*请输入角色名称"
            return render_template('main/role/addroles.html', msg=message)
        role = Role(r_name=r_name)
        role.save()

        return redirect(url_for('main.roles_list'))


@main_blueprint.route('/roleperlist/', methods=['GET'])
@is_login
def role_per_list():
    """角色的权限信息列表"""
    page = int(request.args.get('page', 1))
    # 每页的条数是多少,默认为5条
    page_num = int(request.args.get('page_num', 5))
    if request.method == 'GET':
        r_id = request.args.get('r_id')
        # role = Role.query.filter(Role.r_id == r_id).first()
        # pers = role.permission
        paginate = Permission.query\
            .join(RP, (RP.permission_id == Permission.p_id))\
            .filter(RP.role_id == r_id).paginate(page, page_num)
        pers = paginate.items
        return render_template('main/permission/permissions.html', pers=pers, paginate=paginate)