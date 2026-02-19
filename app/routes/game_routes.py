from flask import Blueprint, request, jsonify
from app.services.word_logic import WordGame
from app.models.word import Word
import secrets
game_bp = Blueprint("game",__name__)
active_games = {}

@game_bp.route("/api/new_game" ,methods = ["POST"])
def new_game():
    random_word = Word.get_random_word()
    if not random_word:
        return jsonify({"error": "No words in database"})
    game_id = secrets.token_urlsafe(16)
    game = WordGame(random_word.word)
    active_games[game_id] = game
    return jsonify({
        "game_id": game_id,
        "word_length":len(random_word.word),
        "category":random_word.category,
        "max_attempts":6
    })
@game_bp.route("/api/guess", methods = ["POST"])
def guess():
    data = request.get_json()
    guess_word= data.get("guess")
    game_id =data.get("game_id")
    if not guess_word:
        return jsonify({"error": "No guess provided"}), 400
    if not game_id or game_id not in active_games:
        return jsonify({"error": "Invalid game ID, start a new game"}), 400
    game = active_games[game_id]
    result = game.MakeGuess(guess_word)
    if result.get("is_over"):
        del active_games[game_id]
    return jsonify(result)

