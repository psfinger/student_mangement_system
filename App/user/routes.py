from functools import wraps

from flask import render_template, session, request, url_for, flash, g
from werkzeug.utils import redirect

from App.user import user_blueprint
from App.models import User, Role
from App.user.forms import RegistrationForm


@user_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.u_id == user_id).first()



# def register():
#     """
#     用户注册页面
#     """
#     if request.method == 'GET':
#         return render_template('user/register.html')
#
#     if request.method == 'POST':
#         # 获取用户填写的信息
#         username = request.form.get('username')
#         pwd1 = request.form.get('pwd1')
#         pwd2 = request.form.get('pwd2')
#
#         # 定义个变量来控制过滤用户填写的信息
#         flag = True
#         # 判断用户是否信息都填写了.(all()函数可以判断用户填写的字段是否有空)
#         if not all([username, pwd1, pwd2]):
#             msg, flag = '* 请填写完整信息', False
#         # 判断用户名是长度是否大于16
#         if len(username) > 16:
#             msg, flag = '* 用户名太长', False
#         # 判断两次填写的密码是否一致
#         if pwd1 != pwd2:
#             msg, flag = '* 两次密码不一致', False
#         # 如果上面的检查有任意一项没有通过就返回注册页面,并提示响应的信息
#         if not flag:
#             return render_template('user/register.html', msg=msg)
#         # 核对输入的用户是否已经被注册了
#         u = User.query.filter(User.username == username).first()
#         # 判断用户名是否已经存在
#         if u:
#             msg = '用户名已经存在'
#             return render_template('user/register.html', msg=msg)
#         # 上面的验证全部通过后就开始创建新用户
#         user = User(username=username, password=pwd1)
#         # 保存注册的用户
#         user.save()
#         # 跳转到登录页面
#         return redirect(url_for('login'))
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册页面
    """
    form = RegistrationForm()
    print("register")
    if form.validate_on_submit():
        print('校验成功')
        user = User(username=form.username.data, password=form.password1.data)
        user.save()
        flash('恭喜您注册成功！')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if request.method == 'GET':
        return render_template('user/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断用户名和密码是否填写
        if not all([username, password]):
            msg = '* 请填写好完整的信息'
            return render_template('user/login.html', msg=msg)
        # 核对用户名和密码是否一致
        user = User.query.filter_by(username=username, password=password).first()
        # 如果用户名和密码一致
        if user:
            # 向session中写入相应的数据
            session['user_id'] = user.u_id
            session['username'] = user.username
            return render_template('index.html')
        # 如果用户名和密码不一致返回登录页面,并给提示信息
        else:
            msg = '* 用户名或者密码不一致'
            return render_template('user/login.html', msg=msg)


@user_blueprint.route('/logout', methods=['GET'])
def logout():
    """
    退出登录
    """
    if request.method == 'GET':
        # 清空session
        session.clear()
        # 跳转到登录页面
        return redirect(url_for('user.login'))


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return check_login


@user_blueprint.route('/userlist/', methods=['GET', 'POST'])
@is_login
def user_list():
    """用户信息列表"""
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = int(request.args.get('page_num', 5))
        paginate = User.query.order_by('u_id').paginate(page, page_num)
        users = paginate.items
        return render_template('user/users.html', users=users, paginate=paginate)


@user_blueprint.route('/adduser/', methods=['GET', 'POST'])
@is_login
def add_user():
    """添加用户信息"""
    if request.method == 'GET':
        return render_template('user/adduser.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        flag = True
        msg = ''
        if not all([username, password1, password2]):
            msg, flag = '请填写完整信息', False
        if len(username) > 16:
            msg, flag = '用户名太长', False
        if password1 != password2:
            msg, flag = '两次密码不一致', False
        if not flag:
            return render_template('user/adduser.html', msg=msg)
        user = User(username=username, password=password1)
        user.save()
        return redirect(url_for('user.user_list'))


@user_blueprint.route('/deluser/', methods=['GET'])
@is_login
def del_user():
    """删除用户"""
    u_id = request.args.get('u_id')
    user = User.query.filter(User.u_id == u_id).first()
    if user:
        user.delete()
    return redirect(url_for('user.user_list'))


@user_blueprint.route('/assignrole/', methods=['GET', 'POST'])
@is_login
def assign_user_role():
    """分配用户权限"""
    if request.method == 'GET':
        u_id = request.args.get('u_id')
        roles = Role.query.all()
        return render_template('user/assign_user_role.html', roles=roles, u_id=u_id)
    if request.method == 'POST':
        r_id = request.form.get('r_id')
        u_id = request.form.get('u_id')
        user = User.query.filter_by(u_id=u_id).first()
        user.role_id = r_id
        user.save()

        return redirect(url_for('user.user_list'))


@user_blueprint.route('/changepwd/', methods=['GET', 'POST'])
@is_login
def change_password():
    """修改用户密码"""
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        return render_template('user/changepwd.html', user=user)

    if request.method == 'POST':
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        pwd3 = request.form.get('pwd3')

        auth = User.query.filter(User.password == pwd1, User.username == username).first()
        if not auth:
            msg = '请输入正确的旧密码'
            return render_template('user/changepwd.html', msg=msg, user=user)
        else:
            if not all([pwd2, pwd3]):
                msg = '密码不能为空'
                return render_template('user/changepwd.html', msg=msg, user=user)
            if pwd2 != pwd3:
                msg = '两次密码不一致,请重新输入'
                return render_template('user/changepwd.html', msg=msg, user=user)
            auth.password = pwd2
            auth.save()
            return redirect(url_for('user.change_pass_sucess'))


@user_blueprint.route('/changepwdsu/', methods=['GET'])
@is_login
def change_pass_sucess():
    """修改密码成功后"""
    if request.method == 'GET':
        return render_template('user/changepwdsu.html')

