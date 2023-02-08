from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from exts import mail, db
from flask_mail import Message
import random
from models import EmailCodeModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from exts import db
# hash加密
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('user', __name__, url_prefix='/user')


# 登录测试
# @bp.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "GET":
#         return render_template('logintest.html')
#     else:
#         user = request.form.get('user')
#         pwd = request.form.get('pwd')
#         print(2)
#         if user == 'admin' and pwd == '123456':
#             print(1)
#             session['user_info'] = user
#             return redirect('/')
#         else:
#             return render_template('logintest.html', msg='用户名或密码输入错误')


# get是从服务器拿数据
# post是提交数据到服务器


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            # 先查有没有这个email
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('用户不存在！')
                return redirect(url_for('user.login'))
            if check_password_hash(user.password, password):
                # flask中的session，是经过加密后存储在cookie中的
                # 使用这个要在config文件中增加SECRET_KEY变量，内容随便输
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('用户名或密码错误，请重新登录！')
                return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf： wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 密码加密存储到数据库中
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            print(form.errors)
            return redirect(url_for('user.register'))


# 默认是get请求,可以用method="POST"改
@bp.route('/email/code')
def get_email_code():
    # 方法一:/email/code/<email>
    # 用方法二：/email/code?email=xxx@qq.com
    email = request.args.get("email")
    code = random.randint(0000, 9999)
    message = Message(subject='邮箱验证码', recipients=[email], body=f'这是验证码：{code}')
    mail.send(message)
    # 下面是存储code
    # 可以用memcached/redis
    # 下面用的是数据库表存储，比上面这个方式更慢
    email_msg = EmailCodeModel(email=email, code=code)
    # 将email_msg添加到会话中
    db.session.add(email_msg)
    # 将内容提交到数据库
    db.session.commit()
    # 返回json格式字符串{"code": 200/400/500, "message": "", "data":""}
    return jsonify({"code": 200, "message": "success", "data": ""})


@bp.route('/mail/test')
def mial_test():
    message = Message(subject='邮箱测试', recipients=['1483836794@qq.com'], body='这是测试邮件')
    mail.send(message)
    return '邮件发送成功！'


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')