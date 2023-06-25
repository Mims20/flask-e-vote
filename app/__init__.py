from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_alembic import Alembic

from app.config import settings

db = SQLAlchemy()
# bcrypt = Bcrypt()
login_manager = LoginManager()
alembic = Alembic()


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{settings.database_username}:{settings.database_password}" \
                                            f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = settings.secret_key

    db.init_app(app)
    # bcrypt.init_app(app)
    login_manager.init_app(app)

    Bootstrap(app)
    alembic.init_app(app)

    from app.routes.main import main
    from app.routes.user import user
    from app.routes.auth import auth
    from app.routes.candidate import candidate
    from app.routes.vote import vote
    from app.routes.result import result
    from app.routes.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(candidate)
    app.register_blueprint(vote)
    app.register_blueprint(result)
    app.register_blueprint(errors)

    return app
