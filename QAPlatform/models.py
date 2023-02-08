from exts import db
from datetime import datetime

# ORM模型映射三步曲
# 1.flask db init; 这步只需要执行一次就行
# 2.flask db migrate; 这步是识别ORM模型的改变,生成迁移脚本
# 3.flask db upgrade; 运行迁移脚本,同步到数据库中


class UserModel(db.Model):
    # 创建表
    __tablename__ = "user"
    # 设置id为整型，为主键，递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 设置为str，最大100字符，不能为空
    username = db.Column(db.String(100), nullable=False)
    # 设置为str，最大100字符，不能为空
    password = db.Column(db.String(200), nullable=False)
    # 设置为str，最大100字符，不能为空，只能唯一存在
    email = db.Column(db.String(100), nullable=False, unique=True)
    # 设置注册时间为数据存入时间
    join_time = db.Column(db.DateTime, default=datetime.now)


class EmailCodeModel(db.Model):
    __tablename__ = 'email_code'
    # 设置id为整型，为主键，递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 设置为str，最大100字符，不能为空，只能唯一存在
    email = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 添加user表的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref='questions')


# 创建评论表
class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 添加外键，用户id，帖子id
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 添加表关系
    question = db.relationship(QuestionModel, backref=db.backref("answers",
                                                                 order_by=create_time.desc()))
    author = db.relationship(UserModel, backref='answers')