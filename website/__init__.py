from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager 
from secrets import SystemRandom

db = SQLAlchemy()
database_name = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key= str(SystemRandom())
    print(app.secret_key)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from .models import User, Note
    create_database(app)
    login_manager= LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    if not path.exists('website/'+database_name):
        db.create_all(app=app)
        print('Database is created!')
        