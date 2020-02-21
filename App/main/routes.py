from flask import request, render_template, session, g
from App.main import main_blueprint
from App.models import User, Grade
from App.user.routes import is_login


@main_blueprint.route('/home/', methods=['GET'])
@is_login
def home():
    """首页"""
    if request.method == 'GET':
        return render_template('index.html')


@main_blueprint.route('/head/', methods=['GET'])
@is_login
def head():
    """页头"""
    if request.method == 'GET':
        return render_template('main/head.html')


@main_blueprint.route('/left/', methods=['GET'])
@is_login
def left():
    """左侧栏"""
    if request.method == 'GET':
        # 获取用户的权限
        permissions = User.query.filter_by(username=g.user.username).first().role.permission
        return render_template('main/left.html', permissions=permissions)



