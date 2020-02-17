from flask import request, render_template, session, g, url_for
from werkzeug.utils import redirect

from App.main import main_blueprint
from App.models import Grade, Student
from App.user.routes import is_login


@main_blueprint.route('/student/', methods=['GET', 'POST'])
@is_login
def student_list():
    """学生信息列表"""
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = int(request.args.get('page_num', 5))
        paginate = Student.query.order_by('s_id').paginate(page, page_num)
        stus = paginate.items
        return render_template('main/student/student.html', stus=stus, paginate=paginate)


@main_blueprint.route('/addstu/', methods=['GET', 'POST'])
@is_login
def add_stu():
    """添加学生"""
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('main/student/addstu.html', grades=grades)

    if request.method == 'POST':
        s_name = request.form.get('s_name')
        s_sex = request.form.get('s_sex')
        grade_id = request.form.get('g_id')
        grades = Grade.query.all()
        if not all([s_name, s_sex, grade_id]):
            msg = '* 请填写好完整的信息'
            return render_template('main/student/addstu.html', grades=grades, msg=msg)
        stu = Student.query.filter(Student.s_name == s_name).first()
        if stu:
            msg = '* 学生姓名不能重复'
            return render_template('main/student/addstu.html', grades=grades, msg=msg)
        stu = Student(s_name=s_name, s_sex=s_sex, grade_id=grade_id)
        stu.save()

        return redirect(url_for('main.student_list'))


@main_blueprint.route('/delstu/', methods=['GET'])
@is_login
def del_stu():
    """删除学生"""
    s_id = request.args.get('s_id')
    stu = Student.query.filter(Student.s_id == s_id).first()
    if stu:
        stu.delete()
    return redirect(url_for('main.student_list'))

