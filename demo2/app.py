# -*- coding:utf-8 -*
# render_template前端渲染
from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)


# 将value格式转换为%Y年%m月%d日 %H:%M
def datetime_f(value, format='%Y年%m月%d日 %H:%M'):
    return value.strftime(format)


# 创建过滤器，过滤器命名为dformat
app.add_template_filter(datetime_f, 'dformat')


class User:
    def __init__(self, username, emil):
        self.username = username
        self.emil = emil


@app.route('/')
def hello():
    user = User('张三', '1187338989@qq.com')
    person = {
        'username': '李四11111',
        'emil': '123456789@qq.com',
    }
    return render_template('index.html', user=user, person=person)


@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template('blog_detail.html', blog_id=blog_id, username='测试')


@app.route('/fitter')
def fittler_demo():
    user = User('张三', '1187338989@qq.com')
    mytime = datetime.now()
    return render_template('fittler.html', user=user, mytime=mytime)


@app.route('/control')
def control():
    age = 19
    books = [{
        'name': '图书1',
        'age': 20
    },{
        'name': '图书2',
        'age': 99
    }]
    return render_template('control.html', age=age, books=books)


@app.route('/child1')
def child1():
    return render_template('child1.html')


@app.route('/child2')
def child2():
    return render_template('child2.html')


@app.route('/static')
def static_demo():
    return render_template('static.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=50)