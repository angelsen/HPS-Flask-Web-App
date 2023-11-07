from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path, getenv
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('POSTGRESS_URL')
    
    db.init_app(app)

    migrate = Migrate(app, db)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .projects import projects as projects_blueprint
    from .location import location_blueprint
    #from .project.project_detail.views import project_detail as project_detail_blueprint
    #from .project.duty_cycle.views import duty_cycle as duty_cycle_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(projects_blueprint, url_prefix='/projects')
    app.register_blueprint(location_blueprint, url_prefix='/location')
    #app.register_blueprint(project_detail_blueprint, url_prefix='/project')
    #app.register_blueprint(duty_cycle_blueprint, url_prefix='/duty-cycle')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app