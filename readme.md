# Word Game

A word guessing game built with Flask and PostgreSQL, inspired by Wordle.

## Modes

**Daily Word**
One word per day, the same for everyone. You get 6 attempts. You can only play once per day (stored in localStorage).

**Streak Mode**
Enter a nick and guess as many words as possible in a row. Each correct guess continues your streak. When you lose, your streak is saved to the leaderboard.

## How to play

1. Pick a mode from the main menu
2. You have 6 attempts to guess the word
3. Category and word length are shown as hints
4. After each guess the letters are colored:
   - Green - correct letter, correct position
   - Yellow - correct letter, wrong position
   - Grey - letter not in the word

## Project structure

```
word_game/
├── app/
│   ├── models/
│   │   ├── word.py         # Word model
│   │   └── score.py        # Score model
│   ├── routes/
│   │   └── game_routes.py  # API endpoints
│   ├── services/
│   │   └── word_logic.py   # Game logic
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/game.js
│   ├── templates/
│   │   └── index.html
│   ├── seeds.py            # Database seed
│   └── __init__.py         # App factory
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run.py
```

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/daily | Get daily word game |
| GET | /api/streak/start?nick= | Start a streak session |
| GET | /api/streak/next?game_id= | Get next word in streak |
| POST | /api/guess | Submit a guess |
| GET | /api/leaderboard | Get top 10 scores |

## Running locally

Requirements: Docker

```bash
docker-compose up --build
```

App runs at http://localhost:5050

## Database

PostgreSQL with two tables:

**words** - id, word, category, date (date is null for streak words, set for daily words)

**scores** - id, nick, streak, date

Words are seeded automatically on first startup from `app/seeds.py`.

## Tech stack

- Python 3.11
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- psycopg2
- HTML / CSS / JavaScript
- Docker / Docker Compose

# License
MIT License
**Author**: Karol Mach