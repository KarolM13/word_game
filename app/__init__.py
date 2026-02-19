from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://admin:simple@db:5432/wordgame')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Blueprint API
    from app.routes.game_routes import game_bp
    app.register_blueprint(game_bp)

    # Route dla strony głównej
    @app.route("/")
    def index():
        return render_template("index.html")
    
    from app.models.word import Word
    
    with app.app_context():
        db.create_all()
        from app.seeds import seed_words
        seed_words()
        print("Dodano przykładowe słowa do bazy!")
    
    return app