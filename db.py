from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class UserDB(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_user(self, username:str, pw:str) -> None:
        self.session.add(User(username=username, password=generate_password_hash(pw, method='sha256')))
        self.session.commit()
        
user_db = UserDB()
        
class User(UserMixin, user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    username = user_db.Column(user_db.String(100), unique=True)
    password = user_db.Column(user_db.String(100))

class DataDB(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_chembl(self, chembl_id:str, smiles:str) -> None:
        self.session.add(Chembl(chembl_id=chembl_id, smiles=smiles))
        self.session.commit()
