from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session

from db import db, User


def create_app():
    app = Flask(__name__)

    # ---------------------------------- SESSION --------------------------------- #
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'  # Temporary hard-drive storage
    Session(app)

    # -------------------------------- APP CONFIG -------------------------------- #
    app.config['SESSION_FILE_THRESHOLD'] = 10
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.secret_key = 'SUKJFIGYRHOWBLUHFFFAOYSANRYYVLZVUVIJVGHUHFFFAOYSAN'  # NaClo-Caffeine

    # ----------------------------------- CORS ----------------------------------- #
    CORS(app, supports_credentials=True)

    # --------------------------------- DATABASE --------------------------------- #
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # ------------------------------- LOGIN MANAGER ------------------------------ #
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = None
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # User primary key (ID) to query for user
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5006', debug=True)
