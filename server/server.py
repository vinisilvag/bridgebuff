from flask import Flask
from flask_cors import CORS
from handlers.game_handler import game_handler
from handlers.rank_handler import rank_handler

app = Flask(__name__)
CORS(app)

app.register_blueprint(game_handler)
app.register_blueprint(rank_handler)

if __name__ == "__main__":
    app.run(debug=True)
