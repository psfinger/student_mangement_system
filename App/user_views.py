from flask import Blueprint, redirect, render_template, request, url_for, session

from App.models import db, User, Grade, Student, Role, Permission

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/create_db/')
def create_db():
    """
    创建数据
    """
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    """
    删除数据库
    """
    db.drop_all()
    return '删除成功'



















