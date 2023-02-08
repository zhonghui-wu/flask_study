# 数据库配置信息
# mysql主机名
HOSTNAME = "127.0.0.1"
# mysql监听端口号
PORT = "3306"
# 连接mysql的用户名
USERNAME = "root"
# 密码
PASSWORD = "123456"
# 连接的数据库名称
DATABASE = "flask_studyqa"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1187338689@qq.com"
MAIL_PASSWORD = "ubtlztgtaybvgici"
MAIL_DEFAULT_SENDER = "1187338689@qq.com"

# 登录session用的密钥
SECRET_KEY = "qwewqe123!@$#$"