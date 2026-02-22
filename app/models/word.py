from app import db
import datetime
class Word(db.Model):
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(25), nullable=False, unique=True)
    category = db.Column(db.String(40), nullable=False)
    date = db.Column(db.Date, nullable=True)

    @classmethod
    def get_random_word(cls, exclude=None):
        import random
        query = cls.query.filter_by(date=None)
        if exclude:
            query = query.filter(~cls.word.in_(exclude))
        words = query.all()
        if words:
            return random.choice(words)
        return None
    
    @classmethod
    def add_word(cls, word, category):
        new_word = cls(word=word, category=category)
        db.session.add(new_word)
        db.session.commit()
        return new_word
    @classmethod
    def get_daily_word(cls):
        today = datetime.date.today()
        return cls.query.filter_by(date=today).first()