from flask import request, render_template, session, g, url_for
from werkzeug.utils import redirect

from App.main import main_blueprint
from App.models import Grade, Student
from App.user.routes import is_login


@main_blueprint.route('/grade/', methods=['GET', 'POST'])
@is_login
def grade_list():
    """
    显示班级列表
    """
    if request.method == 'GET':
        # 查询第几页的数据
        page = int(request.args.get('page', 1))
        # 每页的条数是多少,默认为5条
        page_num = int(request.args.get('page_num', 5))
        # 查询当前第几个的多少条数据
        paginate = Grade.query.order_by('g_id').paginate(page, page_num)
        # 获取某页的具体数据
        grades = paginate.items
        # 返回获取到的班级信息给前端页面
        return render_template('main/grade/grade.html', grades=grades, paginate=paginate)


@main_blueprint.route('/addgrade/', methods=['GET', 'POST'])
@is_login
def add_grade():
    """添加班级"""
    if request.method == 'GET':
        return render_template('main/grade/addgrade.html')

    if request.method == 'POST':
        g_name = request.form.get('g_name')
        g = Grade.query.filter(Grade.g_name == g_name).first()
        # 判断要添加的信息数据库中是否存在(因为班级名称不能重复)
        if g:
            msg = '*班级名称已存在，请重新输入'
            return render_template('main/grade/addgrade.html', msg=msg)
        # 创建班级
        grade = Grade(g_name)
        # 保存班级信息
        grade.save()

        return redirect(url_for('main.grade_list'))


@main_blueprint.route('/edit_grade/', methods=['GET', 'POST'])
@is_login
def edit_grade():
    """编辑班级"""
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        g_name = Grade.query.filter(Grade.g_id == g_id).first().g_name
        return render_template('main/grade/addgrade.html', g_name=g_name, g_id=g_id)

    if request.method == 'POST':
        # 获取需要修改的班级id
        g_id = request.form.get('g_id')
        g_name = request.form.get('g_name')
        # 通过获取到的班级id
        grade = Grade.query.filter(Grade.g_id == g_id).first()
        # 重新给班级赋值
        grade.g_name = g_name
        grade.save()

        return redirect(url_for('main.grade_list'))


@main_blueprint.route('/del_grade/', methods=['GET'])
@is_login
def del_grade():
    """删除班级"""
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        grade = Grade.query.filter(Grade.g_id == g_id).first()
        if grade:
            grade.delete()
    return redirect(url_for('main.grade_list'))


@main_blueprint.route('/grade_student/', methods=['GET'])
@is_login
def grade_students_list():
    """班级中学习的信息列表"""
    page = int(request.args.get('page', 1))
    # 每页的条数是多少,默认为5条
    page_num = int(request.args.get('page_num', 5))
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        paginate = Student.query.filter(Student.grade_id == g_id).order_by('s_id').paginate(page, page_num)
        stus = paginate.items
        return render_template('main/student/student.html', stus=stus, paginate=paginate)

#等待实现
@main_blueprint.route('/del_std_from_grade/', methods=['GET'])
@is_login
def del_std_from_grade():
    """从班级中移除某个学生"""
    if request.method == 'GET':
        s_id = request.args.get('s_id')
        grade = Grade.query.filter(Grade.g_id == g_id).first()
        if grade:
            grade.delete()
    return redirect(url_for('main.grade_list'))
