from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from App.models import User, Grade, Student, Permission, r_p

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/sqlite/studetManagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def init_user_db():
    db.create_all()
    admin = User('l2i', '123')
    print(admin)
    db.session.add(admin)
    db.session.commit()


def init_grade_db():
    db.create_all()
    grade01 = Grade('l2i')
    db.session.add(grade01)
    db.session.commit()


def init_student_db():
    db.create_all()
    std01 = Student('西尔维娅', 0, 2)
    std02 = Student('卡特', 0, 3)
    db.session.add(std01)
    db.session.add(std02)
    db.session.commit()


def init_r_p_db():
    rp05 = r_p(1, 5)
    db.session.add(rp05)
    db.session.commit()


def init_role_db():
    pass


def init_permission_db():
    # db.create_all()
    per01 = Permission('用户列表', 'YHLB')
    db.session.add(per01)
    db.session.commit()


if __name__ == '__main__':
    init_permission_db()
