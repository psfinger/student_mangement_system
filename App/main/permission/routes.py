from flask import request, render_template, url_for
from werkzeug.utils import redirect

from App.main import main_blueprint
from App.models import Permission, db
from App.user.routes import is_login


@main_blueprint.route('/permissions/', methods=['GET'])
@is_login
def permission_list():
    """权限列表"""
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = int(request.args.get('page_num', 5))
        paginate = Permission.query.order_by('p_id').paginate(page, page_num)
        permissions = paginate.items
        return render_template('main/permission/permissions.html', permissions=permissions, paginate=paginate)


@main_blueprint.route('/addpermission/', methods=['GET', 'POST'])
@is_login
def add_permission():
    """添加权限"""
    if request.method == 'GET':
        return render_template('main/permission/addpermission.html')

    if request.method == 'POST':
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')
        if not all([p_name, p_er]):
            msg = '* 请填写好完整的信息'
            return render_template('main/permission/addpermission.html', msg=msg)

        p_name_test_repeat = Permission.query.filter(Permission.p_name == p_name).first()
        if p_name_test_repeat:
            msg = '*权限名称重复'
            return render_template('main/permission/addpermission.html', msg=msg)

        p_er_test_repeat = Permission.query.filter(Permission.p_er == p_er).first()
        if p_er_test_repeat:
            msg1 = '*权限简写名重复'
            return render_template('main/permission/addpermission.html', msg1=msg1)

        permission = Permission(p_name=p_name, p_er=p_er)
        permission.save()

        return redirect(url_for('main.permission_list'))


# 注意这里的/<p_id>
@main_blueprint.route('/eidtpermission/<int:p_id>', methods=['GET', 'POST'])
@is_login
def eidt_permission(p_id, msg=""):
    """编辑权限"""
    per = Permission.query.filter(Permission.p_id == p_id).first()
    if request.method == 'GET':
        return render_template('main/permission/addpermission.html',
                               p_name=per.p_name,
                               p_er=per.p_er,
                               p_id=p_id,
                               msg=msg)
    if request.method == 'POST':
        p_id = request.form.get('p_id')
        p_name = request.form.get('p_name')
        p_er = request.form.get('p_er')
        if not all([p_name, p_er]):
            msg = '* 请填写好完整的信息'
            return render_template('main/permission/addpermission.html',
                                   p_name=per.p_name,
                                   p_er=per.p_er,
                                   p_id=p_id,
                                   msg=msg)
        p_name_test_repeat = Permission.query.filter(Permission.p_name == p_name).first()
        if p_name_test_repeat and p_name != per.p_name:
            msg = '*权限名称重复'
            return render_template('main/permission/addpermission.html',
                                   p_name=per.p_name,
                                   p_er=per.p_er,
                                   p_id=p_id,
                                   msg=msg)

        p_er_test_repeat = Permission.query.filter(Permission.p_er == p_er).first()
        if p_er_test_repeat and p_er != per.p_er:
            msg = '*权限简写名重复'
            return render_template('main/permission/addpermission.html',
                                   p_name=per.p_name,
                                   p_er=per.p_er,
                                   p_id=p_id,
                                   msg=msg)

        per = Permission.query.filter(Permission.p_id == p_id).first()
        per.p_name = p_name
        per.p_er = p_er
        db.session.commit()

        return redirect(url_for('main.permission_list'))


@main_blueprint.route('/delper/', methods=['GET'])
@is_login
def del_per():
    """删除学生"""
    p_id = request.args.get('p_id')
    per = Permission.query.filter(Permission.p_id == p_id).first()
    if per:
        per.delete()
    return redirect(url_for('main.permission_list'))
