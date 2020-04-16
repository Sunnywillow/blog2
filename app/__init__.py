<<<<<<< HEAD
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()  # web框架 用户界面组件
mail = Mail()  # 邮件
moment = Moment()  # 时间
db = SQLAlchemy()  # 数据库

def create_app（config_name):  # 工厂函数
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

=======
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

>>>>>>> fb13ded... Chapter 7: Large file structure (7a)
