import json

from flask import Flask, jsonify, request


def read_scores():
    with open("./scores.jsonl") as f:
        scores = [json.loads(line) for line in f]
        return scores
    return {}


scores = read_scores()

print(scores)

app = Flask(__name__)
app.debug = True


@app.route("/api/game/<int:game_id>", methods=["GET"])
def fetch_game(game_id):
    print("game")
    print("game id", game_id)
    return jsonify()


@app.route("/api/rank/sunk", methods=["GET"])
def rank_sunk(game_id):
    print("sunk")
    print(request.args)
    return jsonify()


@app.route("/api/rank/escaped", methods=["GET"])
def runk_escaped(game_id):
    print("escaped")
    print(request.args)
    return jsonify()


if __name__ == "__main__":
    app.run()
