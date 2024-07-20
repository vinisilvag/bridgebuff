from flask import Blueprint, jsonify
from services.scores import Scores

scores = Scores()

game_handler = Blueprint("game_handler", __name__, url_prefix="/api/game")


@game_handler.route("/<int:game_id>", methods=["GET"])
def fetch_game(game_id):
    game = scores.get_by_id(game_id)
    if not game:
        return (
            jsonify(
                {
                    "error": True,
                    "message": f"Game with id = {game_id} does not exist",
                }
            ),
            404,
        )

    return jsonify({"game_id": game_id, "game_stats": game}), 200
