from flask import Flask, g, session
import config
from exts import db, mail
from models import UserModel
from blueprints.user import bp as user_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# db和app绑定
db.init_app(app)
# db和mail绑定
mail.init_app(app)


migrate = Migrate(app, db)


# 让上方两个bp和app绑定
app.register_blueprint(user_bp)
app.register_blueprint(qa_bp)


# 钩子函数(hook)，就是在正常执行的流程中插入新的内容，先执行这个内容
# before_request / before_first_request / after_request
@app.before_request
def my_before_request():
    # 在登录后拿user_id
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        # 这个g=global,全局变量
        setattr(g, "user", user)
    else:
        # 如果user没有数据则为none
        setattr(g, "user", None)


# 上下文处理器
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50)