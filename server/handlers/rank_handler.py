from flask import Blueprint, jsonify, request
from helpers.paginate import paginate
from helpers.parse_params import parse_query_params
from services.scores import Scores

scores = Scores()

rank_handler = Blueprint("rank_handler", __name__, url_prefix="/api/rank")


@rank_handler.route("/sunk", methods=["GET"])
def rank_sunk():
    limit = request.args.get("limit")
    start = request.args.get("start")

    limit, start, error = parse_query_params(limit, start)
    if error:
        return error

    games = scores.sorted_by_sunk()
    pagination_response = paginate("sunk", games, limit, start)

    return jsonify(pagination_response)


@rank_handler.route("/escaped", methods=["GET"])
def rank_escaped():
    limit = request.args.get("limit")
    start = request.args.get("start")

    limit, start, error = parse_query_params(limit, start)
    if error:
        return error

    games = scores.sorted_by_escaped()
    pagination_response = paginate("escaped", games, limit, start)

    return jsonify(pagination_response)
