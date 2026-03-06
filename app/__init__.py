from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(get_remote_address,default_limits=["200 per day"])



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey123")
    database_url = os.environ.get("DATABASE_URL", "postgresql://admin:simple@db:5432/wordgame")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    from app.routes.game_routes import game_bp
    app.register_blueprint(game_bp)

    @app.route("/")
    def index():
        return render_template("index.html")
    @app.route("/login")
    def login():
        return render_template("login.html")
    with app.app_context():
        from app.models.word import Word
        from app.models.score import Score
        from app.models.user import User
        db.create_all()
        from app.seeds import seed_words
        seed_words()
    
    return app