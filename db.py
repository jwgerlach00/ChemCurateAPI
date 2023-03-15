from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class DB(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_user(self, username:str, pw:str) -> None:
        self.session.add(User(username=username, password=generate_password_hash(pw, method='sha256')))
        self.session.commit()
        
db = DB()
        
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
