from app.models.word import Word
from app import db


def seed_words():
    if Word.query.count() > 0:
        Word.query.delete()
        db.session.commit()
    words = [
            {"word": "Izoyna", "category": "Artist"},
            {"word": "Spazma", "category": "Artist"},
            {"word": "GeezyBeatz", "category": "Artist"},
            {"word": "Lingo", "category": "Artist"},
            {"word": "Pepsi", "category": "Drink"},
            {"word": "Karol", "category": "Name"},
            {"word": "Janusz","category":"Name"},
            {"word": "Tymek", "category": "Name"},
            {"word": "Kizo", "category": "Artist"},
            {"word": "Ola", "category": "Name"},
            {"word":"Szympans", "category": "Animal"},
            {"word": "Bartek", "category": "Name"},
            {"word": "Yeat", "category": "Artist"},
            {"word": "Popek", "category": "Artist"},
            {"word": "Kot","category":"Animal"},
            {"word": "Studio", "category": "Place"}
            ]
    for w in words:
        db.session.add(Word(word=w["word"], category=w["category"]))
    db.session.commit()
    print(f"Seeded {len(words)} words!")

        
    