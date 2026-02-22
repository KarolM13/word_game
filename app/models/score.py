from app import db
import datetime

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(25), nullable=False)
    streak = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today)

    @classmethod
    def add_score(cls, nick, streak):
        new_score = cls(nick=nick, streak=streak, date=datetime.date.today())
        db.session.add(new_score)
        db.session.commit()
        return new_score