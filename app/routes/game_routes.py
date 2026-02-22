from flask import Blueprint, request, jsonify
from app.services.word_logic import WordGame
from app.models.word import Word
from app.models.score import Score
from app import db
import secrets

game_bp = Blueprint("game", __name__)
active_games = {}
active_streaks = {}

@game_bp.route("/api/new_game", methods=["POST"])
def new_game():
    random_word = Word.get_random_word()
    if not random_word:
        return jsonify({"error": "No words in database"})
    game_id = secrets.token_urlsafe(16)
    game = WordGame(random_word.word)
    active_games[game_id] = game
    return jsonify({
        "game_id": game_id,
        "word_length": len(random_word.word),
        "category": random_word.category,
        "max_attempts": 6
    })

@game_bp.route("/api/guess", methods=["POST"])
def guess():
    data = request.get_json()
    guess_word = data.get("guess")
    game_id = data.get("game_id")
    if not guess_word:
        return jsonify({"error": "No guess provided"}), 400
    if not game_id or game_id not in active_games:
        return jsonify({"error": "Invalid game ID, start a new game"}), 400

    is_streak = game_id in active_streaks
    game = active_games[game_id]
    result = game.MakeGuess(guess_word)

    if result.get("is_over"):
        if is_streak:
            streak_data = active_streaks[game_id]
            if result.get("is_won"):
                streak_data["streak"] += 1
                result["streak"] = streak_data["streak"]
                result["next"] = True
            else:
                score = Score(nick=streak_data["nick"], streak=streak_data["streak"])
                db.session.add(score)
                db.session.commit()
                result["streak"] = streak_data["streak"]
                result["next"] = False
                del active_streaks[game_id]
                del active_games[game_id]
        else:
            del active_games[game_id]

    return jsonify(result)

@game_bp.route("/api/daily", methods=["GET"])
def daily_game():
    daily_word = Word.get_daily_word()
    if not daily_word:
        return jsonify({"error": "No daily word for today"})
    game_id = secrets.token_urlsafe(16)
    game = WordGame(daily_word.word)
    active_games[game_id] = game
    return jsonify({
        "game_id": game_id,
        "word_length": len(daily_word.word),
        "category": daily_word.category,
        "max_attempts": 6
    })

@game_bp.route("/api/streak/start", methods=["GET"])
def streak_start():
    nick = request.args.get("nick")
    if not nick:
        return jsonify({"error": "Nick is required"})
    random_word = Word.get_random_word()
    if not random_word:
        return jsonify({"error": "No words in database"}), 400
    game_id = secrets.token_urlsafe(16)
    game = WordGame(random_word.word)
    active_games[game_id] = game
    active_streaks[game_id] = {
        "nick": nick,
        "streak": 0,
        "used_words": [random_word.word]
    }
    return jsonify({
        "game_id": game_id,
        "word_length": len(random_word.word),
        "category": random_word.category,
        "max_attempts": 6,
        "streak": 0
    })

@game_bp.route("/api/streak/next", methods=["GET"])
def streak_next():
    game_id = request.args.get("game_id")
    if not game_id or game_id not in active_streaks:
        return jsonify({"error": "Invalid game_id!"})
    streak_data = active_streaks[game_id]
    used = streak_data["used_words"]
    random_word = Word.get_random_word(exclude=used)
    if not random_word:
        return jsonify({"error": "No more words available"}), 500
    game = WordGame(random_word.word)
    active_games[game_id] = game
    streak_data["used_words"].append(random_word.word)
    return jsonify({
        "game_id": game_id,
        "word_length": len(random_word.word),
        "category": random_word.category,
        "max_attempts": 6,
        "streak": streak_data["streak"]
    })

@game_bp.route("/api/leaderboard", methods=["GET"])
def leaderboard():
    top_scores = Score.query.order_by(Score.streak.desc()).limit(10).all()
    return jsonify([
        {
            "nick": s.nick,
            "streak": s.streak,
            "date": s.date.strftime("%d-%m-%Y")
        } for s in top_scores
    ])
