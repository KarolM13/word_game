from app import db
import datetime
from argon2 import PasswordHasher


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    nick = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(255), nullable =False)
    date = db.Column(db.Date, nullable = False , default = datetime.date.today)

    @classmethod
    def add_user(cls, nick, password):
        psw = PasswordHasher()
        new_user = cls(nick = nick,password = psw.hash(password), date = datetime.date.today())
        db.session.add(new_user)
        db.session.commit()
        return new_user
    @classmethod
    def check_password(cls,nick,password):
        psw = PasswordHasher()
        user = User.query.filter_by(nick=nick).first()
        if user:
            try:
                if psw.verify(user.password,password):
                    return user
            except:
                return None
            return None
                    
        
        
