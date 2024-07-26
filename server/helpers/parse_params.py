from flask import jsonify


def parse_query_params(limit, start):
    limit = limit.strip("{}")
    start = start.strip("{}")
    
    if limit.isdecimal():
        limit = int(limit)
    else:
        return (
            None,
            None,
            (
                jsonify({
                    "error": True,
                    "message": "Limit query param should be an integer",
                }),
                400,
            ),
        )

    if start.isdecimal():
        start = int(start)
    else:
        return (
            None,
            None,
            (
                jsonify({
                    "error": True,
                    "message": "Start query param should be an integer",
                }),
                400,
            ),
        )

    if limit > 50:
        return (
            None,
            None,
            (
                jsonify({
                    "error": True,
                    "message": f"Limit query param should be <= 50, received {limit}",
                }),
                400,
            ),
        )

    if start <= 0:
        return (
            None,
            None,
            (
                jsonify({
                    "error": True,
                    "message": f"Start query param should be > 0, received {start}",
                }),
                400,
            ),
        )

    return limit-1, start-1, None
