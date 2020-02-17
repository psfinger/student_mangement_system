from flask import request, render_template, url_for
from werkzeug.utils import redirect

from App.main import main_blueprint
from App.models import Permission, db
from App.user.routes import is_login


@main_blueprint.route('/permissions/', methods=['GET', 'POST'])
@is_login
def permission_list():
    """权限列表"""
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('permissions.html', permissions=permissions)


@main_blueprint.route('/addpermission/', methods=['GET', 'POST'])
@is_login
def add_permission():
    """添加权限"""
    if request.method == 'GET':
        pers = Permission.query.all()
        return render_template('addpermission.html', pers=pers)

    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')

        p_name_test_repeat = Permission.query.filter(Permission.p_name == p_name).first()
        if p_name_test_repeat:
            msg = '*权限名称重复'
            return render_template('addpermission.html', msg=msg)

        p_er_test_repeat = Permission.query.filter(Permission.p_er == p_er).first()

        if p_er_test_repeat:
            msg1 = '*权限简写名重复'
            return render_template('addpermission.html', msg1=msg1)

        permission = Permission(p_name=p_name, p_er=p_er)
        permission.save()

        return redirect(url_for('user.permission_list'))


@main_blueprint.route('/eidtorpermission/', methods=['GET', 'POST'])
@is_login
def eidtor_permission():
    """编辑权限"""
    if request.method == 'GET':
        p_id = request.args.get('p_id')
        pers = Permission.query.filter(Permission.p_id == p_id).first()
        return render_template('addpermission.html', pers=pers, p_id=p_id)
    if request.method == 'POST':
        p_id = request.form.get('p_id')
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')

        p_name_test_repeat = Permission.query.filter(Permission.p_name == p_name).first()
        if p_name_test_repeat:
            msg = '*权限名称重复'
            pers = Permission.query.all()
            return render_template('addpermission.html', msg=msg, pers=pers)

        p_er_test_repeat = Permission.query.filter(Permission.p_er == p_er).first()

        if p_er_test_repeat:
            msg1 = '*权限简写名重复'
            pers = Permission.query.all()
            return render_template('addpermission.html', msg1=msg1, pers=pers)

        per = Permission.query.filter(Permission.p_id == p_id).first()
        per.p_name = p_name
        per.p_er = p_er
        db.session.commit()

        return redirect(url_for('user.permission_list'))