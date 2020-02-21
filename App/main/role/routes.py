from flask import request, render_template, url_for
from werkzeug.utils import redirect

from App.main import main_blueprint
from App.models import Role, Permission, RP, db
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


@main_blueprint.route('/delroles/', methods=['GET', 'POST'])
@is_login
def del_roles():
    """删除角色"""
    r_id = request.args.get('r_id')
    role = Role.query.filter(Role.r_id == r_id).first()
    if role:
        role.delete()
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
        # 上面一种方法可以列出role的所有权限，得到的是一个list对象，无法使用paginate方法
        paginate = Permission.query\
            .join(RP, (RP.permission_id == Permission.p_id))\
            .filter(RP.role_id == r_id).paginate(page, page_num)
        pers = paginate.items
        return render_template('main/role/role_per_list.html', permissions=pers, paginate=paginate)


@main_blueprint.route('/addroleper/', methods=['GET', 'POST'])
@is_login
def add_role_per():
    """添加角色权限"""
    r_id = request.args.get('r_id')
    role = Role.query.get(r_id)
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('main/role/add_role_per.html', permissions=permissions, r_id=r_id, r_name=role.r_name)

    if request.method == 'POST':
        p_id = request.form.get('p_id')
        # 获取权限对象
        per = Permission.query.get(p_id)
        # 添加对应的角色和权限的对应关系
        per.roles.append(role)
        db.session.add(per)
        db.session.commit()

        return redirect(url_for('main.roles_list'))


@main_blueprint.route('/subroleper/', methods=['GET', 'POST'])
@is_login
def sub_role_per():
    """减少用户权限"""
    if request.method == 'GET':
        r_id = request.args.get('r_id')
        pers = Role.query.filter(Role.r_id == r_id).first().permission
        return render_template('main/role/role_per_list.html', pers=pers, r_id=r_id)

    if request.method == 'POST':
        r_id = request.args.get('r_id')
        p_id = request.form.get('p_id')
        role = Role.query.get(r_id)
        per = Permission.query.get(p_id)

        # 解除角色和权限的对应关系
        per.roles.remove(role)
        db.session.commit()

        pers = Role.query.filter(Role.r_id == r_id).first().permission
        return render_template('main/role/role_per_list.html', pers=pers, r_id=r_id)