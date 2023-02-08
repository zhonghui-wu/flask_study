import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCodeModel
from exts import db


# Form: 主要就是用来验证前端提交的数据是否符合要求
# pip install email_validator
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    code = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码格式错误')])
    username = wtforms.StringField(validators=[Length(min=2, max=20, message='用户名格式错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误')])
    # 二次确认密码
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='两次密码不一致')])

    # 自定义验证，
    # 1.验证邮箱是否注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已被注册')

    # 2.验证邮箱验证码是否正确
    def validate_code(self, field):
        code = field.data
        email = self.email.data
        code_model = EmailCodeModel.query.filter_by(email=email, code=code).first()
        if not code_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误！')
        else:
            # 如果验证码正确就从数据库删掉该验证码
            db.session.delete(code_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=2, max=200, message='标题格式错误')])
    content = wtforms.StringField(validators=[Length(min=1, max=2000, message='内容格式错误')])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, max=2000, message='内容格式错误')])
    question_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入问题id')])