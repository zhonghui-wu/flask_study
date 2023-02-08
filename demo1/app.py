from flask import Flask,request

# __name__代表当前文件模块
app = Flask(__name__)


# 创建一个路由和视图函数的映射
@app.route('/home')
def home():
    return '我是首页'


@app.route('/personal')
def personal():
    return '我是个人中心'


# 查询字符串方式传参
@app.route('/blog/list')
def blog_list():
    page = request.args.get('page', default=1, type=int)
    return f'我是博客第{page}页列表'


@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    return '您访问的博客id是：%s' % blog_id


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50)