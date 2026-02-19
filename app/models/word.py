from app import db

class Word(db.Model):
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(25), nullable=False, unique=True)
    category = db.Column(db.String(40), nullable=False)
    
    def __repr__(self):
        return f'<Word {self.word}>'
    
    @classmethod
    def get_random_word(cls):
        import random
        words = cls.query.all()
        if words:
            return random.choice(words)
        return None
    
    @classmethod
    def add_word(cls, word, category):
        """Dodaj nowe słowo do bazy"""
        new_word = cls(word=word, category=category)
        db.session.add(new_word)
        db.session.commit()
        return new_word