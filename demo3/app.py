from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate


app = Flask(__name__)


# mysql主机名
HOSTNAME = "127.0.0.1"
# mysql监听端口号
PORT = "3306"
# 连接mysql的用户名
USERNAME = "root"
# 密码
PASSWORD = "123456"
# 连接的数据库名称
DATABASE = "flask_learn"

app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ORM模型映射三步曲
# 1.flask db init; 这步只需要执行一次就行
# 2.flask db migrate; 这步是识别ORM模型的改变,生成迁移脚本
# 3.flask db upgrade; 运行迁移脚本,同步到数据库中


# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("SELECT 1"))
#         print(rs.fetchone())  # 查看是否连接成功,连接成功后打印1


class User(db.Model):
    # 创建表内容
    __tablename__ = 'user'
    # 设置id为整型，设置为主键，设置自动递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 设置username为str类型最大100位数，不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))


class Article(db.Model):
    # 创建表内容
    __tablename__ = 'acticle'
    # 设置id为整型，设置为主键，设置自动递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # backref: 会自动给User模型添加一个articles 的属性，用来获取文章列表
    author = db.relationship("User", backref='articles')


# with app.app_context():
#     # 执行上面的创建表代码,缺点是新增表时无法同步新增,不用这个方法
#     db.create_all()


@app.route('/user/add')
def add_user():
    # 创建ORM对象
    user = User(username='张三', password='111111')
    # user = User(username='李四', password='222222')
    # 将ORM对象添加到db.session中
    db.session.add(user)
    # 再将db.session同步到数据库中
    db.session.commit()
    return '用户创建成功！'


@app.route('/user/query')
def query_user():
    # get查找:根据主键查找，只查找一条数据
    # user = User.query.get(1)
    # print(f'{user.id}:{user.username}--{user.password}')

    # filert_by查找，返回是个类数组，可用以下标/切片
    users = User.query.filter_by(username='张三')
    for user in users:
        print(user.username, user.password)
    return '查找成功'


@app.route('/user/update')
def update_user():
    user = User.query.filter_by(username='李四').first()
    user.password = '333333'
    db.session.commit()
    return '密码修改成功'


@app.route('/user/delete')
def delete_user():
    # 查找
    user = User.query.get(1)
    # 从db.session中删除
    db.session.delete(user)
    # 将db.session中的修改同步到数据库
    db.session.commit()
    return "数据删除成功！"


@app.route('/article/add')
def article_add():
    article1 = Article(title='FLask学习大纲', content='Flaskxxxxxx...')
    article2 = Article(title='Django学习大纲', content='Djangoxxxxxx...')
    article1.author = User.query.get(2)
    article2.author = User.query.get(2)
    db.session.add_all([article2, article1])
    db.session.commit()
    return '文章添加成功！'


@app.route('/article/query')
def query_article():
    # 先根据id查到用户下的所有文章
    user = User.query.get(2)
    # 再遍历文章
    for article in user.articles:
        print(article.title, article.content)
    return '文章查找成功'


@app.route('/')
def home():
    return '欢迎来到首页'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)