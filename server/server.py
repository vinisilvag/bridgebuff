from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from handlers.game_handler import game_handler
from handlers.rank_handler import rank_handler

app = Flask(__name__)
CORS(app)

swaggerui_handler = get_swaggerui_blueprint(
    "/api/docs",
    "/static/swagger.json",
)

app.register_blueprint(swaggerui_handler)
app.register_blueprint(game_handler)
app.register_blueprint(rank_handler)


if __name__ == "__main__":
    app.run(debug=True)
