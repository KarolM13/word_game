from app.models.word import Word
from app import db
import datetime

def seed_words():
    if Word.query.count() > 0:
        return
    today = datetime.date.today()
    words = [
            #Daily words
            {"word": "Rosół", "category": "Food", "date": today},
            {"word": "Zupa", "category": "Food", "date": today + datetime.timedelta(days=1)},
            {"word": "Okekel", "category": "Artist", "date": today + datetime.timedelta(days=2)},
            {"word": "Pierogi", "category": "Food", "date": today + datetime.timedelta(days=3)},
            # Streak words
            {"word": "Izonya", "category": "Artist", "date": None},
            {"word": "Spazma", "category": "Artist", "date": None},
            {"word": "GeezyBeatz", "category": "Artist", "date": None},
            {"word": "Lingo", "category": "Artist", "date": None},
            {"word": "Pepsi", "category": "Drink", "date": None},
            {"word": "Pizza", "category": "Food", "date": None},
            {"word": "Janusz", "category": "Name", "date": None},
            {"word": "Dog", "category": "Animal", "date": None},
            {"word": "Kizo", "category": "Artist", "date": None},
            {"word": "Spotify", "category": "App", "date": None},
            {"word": "Szympans", "category": "Animal", "date": None},
            {"word": "Discord", "category": "App", "date": None},
            {"word": "Yeat", "category": "Artist", "date": None},
            {"word": "Popek", "category": "Artist", "date": None},
            {"word": "Kot", "category": "Animal", "date": None},
            {"word": "Studio", "category": "Place", "date": None}
            ]
    for w in words:
        db.session.add(Word(word=w["word"], category=w["category"], date=w["date"]))
    db.session.commit()
    print(f"Seeded {len(words)} words!")

        
    